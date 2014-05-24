---
layout: post
title:  "Oops, I partitioned my drive.."
date:   2013-05-29 14:48:00
---


I
 did something colossally stupid yesterday.  I was at the local
hackerspace, hoping to cut some acrylic, and the wifi wasn't working.  I
 was in a hurry and frustrated, so I pulled out a USB stick and tried to
 erase it.  Suffice to say, the USB stick wasn't at `/dev/sda`.  I
 wiped out the GPT on my laptop.  Its disk is encrypted, so the buffer
store kept things working for a while, then suddenly I had a blinking
root prompt and .. nothing.

After
 the obligatory cold-sweat had passed, I quietly packed up and walked
out.  Here's the story of how I recovered from this, with the help of
Jake Watkins (:dividehex). The system didn't have any irrecoverable data
 on it.  All of my work is in version-control, and I'm religious about
pushing to github.  Even my home directory's dotfiles are on github (in a
 private repo).  But I spent several weeks setting this laptop up (Linux
 on the desktop is only usable from a very long-term perspective!), and
unfortunately one of the few things that wasn't in version control was
my notes on how I'd done so.  Rebuilding this from scratch would take a
few weeks and make a very grumpy Dustin.

To
make things interesting, this ThinkPad X1 Carbon has no Ethernet port.
It's wifi only.  There are dongles available from Lenovo, but I don't
have one.

## Backup

OK, so let's stop the bleeding.

I
booted from the Fedora Live USB stick I'd used to install the system
initially.  Once it was up, I schlepped the entire drive over to my
desktop:

    ssh root@ramanujan dd if=/dev/sda > laptop-disk.img

That
took about 8 hours, but that gave me time to do some other research,
conduct a Baltic Porter tasting (multitasking!), and sleep.

## Find the Data

So
the situation is that I have a partition table with a single 256G FAT32
partition in it.  Somewhere on the disk, my data is probably still
intact.  But where?

Jake suggested looking for the GPT backup table, which is at the end of the disk.  The `gdisk` advanced options allow you to examine this table, but it too was empty.

Jake's other suggestion was to look for the signature of the LUKS crypto container.

    dd if=/dev/sda | od -c | grep 'L   U   K   S'

This
eventually turned up the beginning of the partition, 05364000000
(decimal 735051776) bytes into the disk.  Dividing that by 512, the size
 of a sector, that's sector 1435648.

In `gdisk`, I created a partition beginning at that location and running to the end of the disk.

    # cryptsetup luksDump /dev/sda1
    LUKS header information for /dev/sda1

    Version:        1
    Cipher name:    aes
    Cipher mode:    xts-plain64
    Hash spec:      sha1
    Payload offset: 4096
    MK bits:        512
    MK digest:      e2 f9 fa 7d 44 dc 82 f5 3c 39 1d e2 ac 6e e3 d2 d0 f5 2b 1b
    MK salt:        05 8b a0 ee 7a bf 37 73 7b 15 c1 7a 41 0b 46 19
                    56 68 e1 36 f7 7c b3 d0 74 bf 21 98 a1 e6 75 7b
    MK iterations:  13750
    UUID:           4057691b-b580-4d05-afd3-9e2efe8d65d3
    ...

so it looks like I've found the data.

    # cryptsetup luksOpen /dev/sda1 secret

    # mount /dev/mapper/secret /mnt

This
didn't work.  It's not an ext4 volume - it's an LVM physical volume.
Udev has already run the pvscan, so I just need to activate the volume
group:

    # vgscan -a y fedora
    # mount /dev/fedora/root /mnt
    # mount /dev/fedora/home /mnt/home

At
this point, it's time for another backup.  I used tar to dump the
contents of both partitions, storing the tarball on my desktop machine.
 This took about an hour.  Now I feel a lot better -- I have my notes
from customizing the system, and anything else that's not backed up that
 I might have forgotten.  But I haven't actually lost any data - can I
recover this completely?

## Rebuild It

I
reboot the Live USB stick, just to reset all of the partition maps, luks
 opens, etc. that I had done.  I realize that /dev/sda1 is probably not
the right partition number for the full filesystem, so I move that to
/dev/sda3 (by deleting and re-creating with the same first/last
sectors).  Another reboot.

When it starts up again, I fire up the installer and tried to install _around_
 the existing data.  I figure I can do a minimal installation in some of
 the free space, particularly since Anaconda reassured me that it only
needed 3.1G.

Long
story short, this was a lie.  Anaconda is a horrible piece of software,
with bugs galore.  For example, if you set a partition's size, it will
randomly make up another size and use that instead.  Ugh.

It
turns out, Anaconda needs about 15G to do the install.  So, I need to
shrink /dev/sda3 by at least that much.  I resize logical volumes all
the time, but this is the reverse -- I need to shrink a physical volume.
  That turns out to be a bit tricky.  First, after opening the LUKS
volume, I run `pvresize`:

    pvresize --setphysicalvolumesize 210g /dev/mapper/secret

This
fails, telling me that there are extents beyond the new last extent.
Subtract a few from that last extent and call that $boundary.  Run `pvdisplay /dev/mapper/secret` to get the total physical extents, and call that $total.  Then, use `pvmove` to shift those around:

    pvmove --alloc anywhere /dev/mapper/secret:$boundary-$total /dev/mapper/secret:0-$boundary

and I re-run the `pvresize` command.

Now, I
 resize the LUKS container that PV is housed in.  This requires a little
 arithmetic.  LVM uses "GiB", which are the normal power-of-two things,
not the stupid disk-manufacturer power-of-ten things.  So 210g is
225485783040 bytes, which (divided by 512) is 440401920 sectors.

    cryptsetup resize --size 440401920 /dev/mapper/secret

OK, I
 shrank the PV, I shrank the enclosing LUKS container, and now I need to
 shrink the partition.  This means deleting and re-adding the partition
in gdisk.  The starting sector stays the same, while the last sector is
calculated as $starting_sector + 440401920 - 1\.  The -1 is important
there - I'm specifying the _last_sector, not the first sector of
the next partition.  That'd be a sad way to lose 512 bytes of data when I
 least expect it.  The filesystem type doesn't seem to matter - I used
the default, but I noticed that Anaconda uses 0700.

Reboot
 and run the install again.  Let Anaconda do its thing, because it's not
 going to listen to me if I try to customize it.  Anaconda happened to
choose a different VG name (fedora_ramanujan) for the new volume group.
 If it hadn't, I might have had to rename things.  Reboot, and I have a
fresh system.

If I was smart, I would have run 'yum upgrade' now, but I didn't.  More on that in a second.

The
idea is that I now have UEFI set up, and all of the proper boot
partitions, but it's running from the wrong encrypted partition.
Changing that is as simple as editing /boot/efi/EFI/fedora/grub.cfg,
replacing the new VG name with the old VG name, and the new LUKS UUID
with the old LUKS UUID (from 'cryptsetup dumpLuks').  Reboot, enter my
passphrase, and .. "Welcome to emergency mode!".  A bit of poking around
 shows that all of my partitions are mounted properly, but the journal
shows failures mounting /boot/efi, because of a missing vfat module.

## Kernel Woes

The kernel and initrd are, of course, on /boot, and are the version installed from the Live USB stick.  The kernel _modules_ are on /, and are the updated versions from several months later.  They don't match up.

The
quick fix is to mount the new LUKS container and copy /lib/modules over
/lib/modules on the old container.  This gets me a copy of all of the
modules that Anaconda had installed, and lets me boot all the way into a
 working system .. almost.  The wifi isn't working.

This
is probably because I'm running an old kernel version with an
otherwise-updated system.  Upgrading to the latest kernel is the fix.
That's tricky with no wifi, so I look up the packages on my desktop,
throw them on a USB stick (being very careful not to re-partition my
desktop's HDD in the process!), and run

    yum reinstall /mnt/usb/kernel-*

on the laptop once the USB stick is mounted there.  Reboot, and all is back to normal.

That was not the most fun I've ever had in 20 hours.  But it was an adventure.

