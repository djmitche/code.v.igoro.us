---
layout: post
title:  "Building a partitioned log table"
date:   2012-09-13 10:46:00
---


For
 a project at Mozilla that involves re-imaging hundreds of mobile
devices, we want to gather logs in a database for failure analysis.
Mobile devices fail all the time -- not sure if you knew that.

We'll
 probably end up with 1,000-10,000 log entries per day.  We'd like to
expire them on a relatively aggressive schedule -- no need for
historical analysis at this level.  So that means not only a lot of
inserts, but a lot of deletes.

We're
 using MySQL as the database backend, and MySQL doesn't do well with
deletes - it just marks the row as deleted, but doesn't reclaim the
space, and in fact doesn't even remove the row from consideration in
queries.  So if you blindly insert and delete in a table, MySQL will eat
 disk space and get progressively slower.

One
fix to this is to optimize the table periodically.  However, this
requires a full lock of the table for the duration of the optimize,
which can be quite a while.  We dont' want to cause a backup of
production tasks while this is going on.

The
other option is to partition the table.  A partitioned table is
basically a set of tables (partitions) with the same columns, organized
to look like a single table.  There's a partitioning function that
determines in which partition a particular row belongs.  There are a few
 advantages.  Each partition is a fraction of the size of the whole
table, so inserts are quicker (once the appropriate table is
determined).  The query engine can use "partition pruning" to ignore
partitions that could not hold rows relevant to the query.  Finally,
dropping an entire partition at once is a very simple operation, and
doesn't leave any garbage  that needs to be optimized away.

For
logs, we want to partition by time, in this case with one partition per
day.   Most of the "get the logs" queries will use a limited time range,
 invoking query pruning and allowing a quick response.

The
tricky part is, the DB server does not automatically create and destroy
partitions.  We need to do that.  It's pretty straightforward with
stored procedures, though.  Here's the resulting SQL to create the logs
table:

    DROP TABLE IF EXISTS logs;
    CREATE TABLE logs (
        -- foreign key for the board
        board_id integer not null,
        ts timestamp not null,
        -- short string giving the origin of the message (syslog, api, etc.)
        source varchar(32) not null,
        -- the message itself
        message text not null,
        -- indices
        index board_id_idx (board_id),
        index ts_idx (ts)
    );

    --
    -- automated log partition handling
    --

    DELIMITER $$

    -- Procedure to initialize partitioning on the logs table
    DROP PROCEDURE IF EXISTS init_log_partitions $$
    CREATE PROCEDURE init_log_partitions(days_past INT, days_future INT)
    BEGIN
        DECLARE newpart integer;
        SELECT UNIX_TIMESTAMP(NOW()) INTO newpart;
        SELECT newpart - (newpart % 86400) INTO newpart; -- round down to the previous whole day

        -- add partitions, with a single partition for the beginning of the current day, then
        -- let update_log_partitions take it from there
        SET @sql := CONCAT('ALTER TABLE logs PARTITION BY RANGE (UNIX_TIMESTAMP(ts)) ('
                            , 'PARTITION p'
                            , CAST(newpart as char(16))
                            , ' VALUES LESS THAN ('
                            , CAST(newpart as char(16))
                            , '));');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        -- do an initial update to get things synchronized
        call update_log_partitions(days_past, days_future);
    END $$

    -- Procedure to delete old partitions and create new ones around the current date
    DROP PROCEDURE IF EXISTS update_log_partitions $$
    CREATE PROCEDURE update_log_partitions(days_past INT, days_future INT)
    BEGIN
        DECLARE part integer;
        DECLARE newpart integer;
        DECLARE earliest integer;
        DECLARE latest integer;

        -- add new partitions; keep adding a partition for a new day until we reach latest
        SELECT UNIX_TIMESTAMP(NOW()) + 86400 * (days_future+1) INTO latest;
        createloop: LOOP
            -- Get the newest partition (PARTITION_DESCRIPTION is the number from VALUES LESS THAN)
            -- partitions are named similarly, with a 'p' prefix
            SELECT MAX(PARTITION_DESCRIPTION) INTO part
                FROM INFORMATION_SCHEMA.PARTITIONS
                WHERE TABLE_NAME='logs'
                AND TABLE_SCHEMA='imagingservice';
            IF part < latest THEN -- note part cannot be NULL, as there must be at least one partition
                SELECT part + 86400 INTO newpart;
                SET @sql := CONCAT('ALTER TABLE logs ADD PARTITION ( PARTITION p'
                                    , CAST(newpart as char(16))
                                    , ' VALUES LESS THAN ('
                                    , CAST(newpart as char(16))
                                    , '));');
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            ELSE
                LEAVE createloop;
            END IF;
        END LOOP;

        -- now, deal with pruning old partitions; select the minimum partition
        -- and delete it if it's too old
        SELECT UNIX_TIMESTAMP(NOW()) - 86400 * (days_past+1) INTO earliest;
        purgeloop: LOOP
            -- Get the oldest partition
            SELECT MIN(PARTITION_DESCRIPTION) INTO part
                FROM INFORMATION_SCHEMA.PARTITIONS
                WHERE TABLE_NAME='logs'
                AND TABLE_SCHEMA='imagingservice';
            IF part < earliest THEN
                SET @sql := CONCAT('ALTER TABLE logs DROP PARTITION p'
                                    , CAST(part as char(16))
                                    , ';');
                PREPARE stmt FROM @sql;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
            ELSE
                LEAVE purgeloop;
            END IF;
        END LOOP;
    END $$

    DELIMITER ;

    -- initialize the partitioning
    CALL init_log_partitions(14, 1);

    -- and then update every day (this can't be set up in init_log_partitions)
    DROP EVENT IF EXISTS update_log_partitions;
    CREATE EVENT update_log_partitions  ON SCHEDULE EVERY 1 day
    DO CALL update_log_partitions(14, 1);

A few
 notes here.  First, the table is created without any partitions.  This
is because I don't know a priori which partitions it should have, and
it's easier to get code to figure that out than do it myself.  That's
what the `init_log_partitions` function does.  The `update_log_partitions`
 function looks at the current time and makes sure there are enough
partitions for the future, and drops partitions too far in the past.
Finally, a MySQL event is set up to update the partitions daily.

You'll need to enable the event scheduler globally to get this to run:

    set global event_scheduler=on;

