---
title: 'Redeploying Taskcluster: Hosted vs. Shipped Software'
layout: post
date:   2018-05-21 15:00:00
categories: [mozilla,taskcluster]
---

The Taskcluster team's work on
[redeployability](http://code.v.igoro.us/posts/2018/01/r14y.html) means
switching from a *hosted* service to a *shipped* application.

A hosted service is one where the authors of the software are also running the
main instance of that software. Examples include Github, Facebook, and
[Mozillians](https://mozillians.org). By contrast, a shipped application is
deployed multiple times by people unrelated to the software's authors. Examples
of shipped applications include Gitlab, Joomla, and the Rust toolchain. And, of
course, Firefox!

## Hosted Services

Operating a hosted service can be liberating. Blog posts describe the joys of
[continuous
deployment](https://blog.github.com/2012-08-29-deploying-at-github/) -- even
deploying the service multiple times per day. Bugs can be fixed quickly, either
by rolling back to a previous deployment or by deploying a fix.

Deploying new features on a hosted service is pretty easy, too. Even a complex
change can be broken down into phases and accomplished without downtime. For
example, changing the backend storage for a service can be accomplished by
modifying the service to write to both old and new backends, mirroring existing
data from old to new, switching reads to the new backend, and finally removing
the code to write to the old backend. Each phase is deployed separately, with
careful monitoring.  If anything goes wrong, rollback to the old backend is
quick and easy.

Hosted service developers are often involved with operation of the service, and
operational issues can frequently be diagnosed or even corrected with
modifications to the software. For example, if a service is experiencing
performance issues due to particular kinds of queries, a quick deployment to
identify and reject those queries can keep the service up, followed by a patch
to add caching or some other approach to improve performance.

## Shipped Applications

A shipped application is sent out into the world to be used by other people.
Those users may or may not use the latest version, and certainly will not
update several times per day (the heroes running Firefox Nightly being a
notable exception). So, many versions of the application will be running
simultaneously. Some applications support automatic updates, but many users
want to control when -- and if -- they update. For example, upgrading a website
built with a CMS like Joomla is a risky operation, especially if the website
has been heavily customized.

Upgrades are important both for new features and for bugfixes, including for
security bugs. An instance of an application like Gitlab might require an
immediate upgrade when a security issue is discovered. However, especially if
the deployment is several versions old, that critical upgrade may carry a great
deal of risk. Producers of shipped software sometimes provide backported fixes
for just this purpose, at least for long term support (LTS) or extended support
release (ESR) versions, but this has a substantial cost for the application
developers.

Upgrading services like Gitlab or Joomla is made more difficult because there
is lots of user data that must remain accessible after the upgrade. For major
upgrades, that often requires some kind of migration as data formats and
schemas change.  In cases where the upgrade spans several major versions, it
may be necessary to apply several migrations in order. Tools like Alembic help
with this by maintaining and applying step-by-step database migrations.

## Taskcluster

Today, Taskcluster is very much a hosted application. There is only one
"instance" of Taskcluster in the world, at [taskcluster.net](https://taskcluster.net).
The Taskcluster team is responsible for both development and operation of the
service, and also works closely with the Firefox build team as a user of the
service.

We want to make Taskcluster a shipped application. As the descriptions above
suggest, this is not a simple process. The following sections highlight some
of the challenges we are facing.

### Releases and Deployment

We currently deploy Taskcluster microservices independently. That is, when we
make a change to a service like taskcluster-hooks, we deploy an upgrade to that
service without modifying the other services. We often sequence these changes
carefully to ensure continued compatibility: we expect only specific
combinations of services to run together.

This is a far more intricate process than we can expect users to follow.
Instead, we will ship Taskcluster *releases* comprised of a set of built Docker
images and a spec file identifying those images and how they should be
deployed. We will test that this particular combination of versions works well
together.

Deploying a release involves combining that spec file with some
deployment-specific configuration and some infrastructure information
(implemented via [Terraform](http://terraform.io/)) to produce a set of
[Kubernetes](http://kubernetes.io/) resources for deployment with `kubectl`.
Kubernetes and Terraform both have limited support for migration from one
release to another: Terraform will only create or modify changed resources, and
Kubernetes will perform a phased roll-out of any modified resources.

By the way, all of this build-and-release functionality is implemented in the
new [taskcluster-installer](https://github.com/taskcluster/taskcluster-installer).

### Service Discovery

The string `taskcluster.net` appears quite frequently in the Taskcluster source
code. For any other deployment, that hostname is not valid -- but how will the
service find the correct hostname? The question extends to determining pulse
exchange names, task artifact hostnames, and so on. There are also security
issues to consider: misconfiguration of URLs might enable XSS and CSRF attacks
from untrusted content such as task artifacts.

The approach we are taking is to define a `rootUrl` from which all other URLs
and service identities can be determined. Some are determined by simple
transformations encapsulated in a new
[taskcluster-lib-urls](https://github.com/taskcluster/taskcluster-lib-urls)
library. Others are fetched at runtime from other services: pulse exchanges
from the taskcluster-pulse service, artifact URLs from the taskcluster-queue
service, and so on.

The `rootUrl` is a single domain, with all Taskcluster services available at
sub-paths such as `/api/queue`. Users of the current Taskcluster installation
will note that this is a change: queue is currently at
`https://queue.taskcluster.net`, not `https://taskcluster.net/queue`. We have
solved this issue by special-casing the rootUrl `https://taskcluster.net` to
generate the old-style URLs. Once we have migrated all users out of the current
installation, we will remove that special-case.

### Data Migrations

The first few deployments of Taskcluster will not require great support for
migrations. A staging environment, for example, can be completely destroyed and
re-created without any adverse impact.  But we will soon need to support users
upgrading Taskcluster from earlier releases with no (or at least minimal)
downtime.

Our Azure tables library
([azure-entities](https://github.com/taskcluster/azure-entities)) already has
rudimentary support for schema updates, so modifying the structure of table
rows is not difficult, although refactoring a single table into multiple tables
would be difficult.

As we transition to using Postgres instead of Azure, we will need to adopt some
of the common migration tools. Ideally we can support downtime-free upgrades
like azure-entities does, instead of requiring downtime to run DB migrations
synchronously. [Bug 1431783](https://bugzilla.mozilla.org/show_bug.cgi?id=1431783)
tracks this work.

### Customization

As a former maintainer of Buildbot, I've had a lot of experience with CI
applications as they are used in various organizations. The surprising
observation is this: every organization thinks that their approach to CI is the
obvious and only way to do things; and every organization does things in a
radically different way. Developers gonna develop, and any CI framework *will*
get modified to suit the needs of each user.

Lots of Buildbot installations are heavily customized to meet local needs. That
has caused a lot of Buildbot users to get "stuck" at older versions, since
upgrades would conflict with the customizations. Part of this difficulty is due
to a failure of the Buildbot project to provide strong guidelines for
customization. Recent versions of Buildbot have done better by providing
clearly documented APIs and marking other interfaces as private and subject to
change.

Taskcluster already has strong APIs, so we begin a step ahead. We might consider
additional guidelines:

* Users should not customize existing services, except to make experimental
  changes that will eventually be merged upstream.  This frees the Taskcluster
  team to make changes to services without concern that those will conflict with
  users' modifications.

* Users are encouraged, instead, to develop their own services, either hosted
  within the Taskcluster deployment as a site-specific service, or hosted
  externally but following Taskcluster API conventions. A local example is the
  [tc-coalesce](https://github.com/mozilla/tc-coalesce) service, developed by
  the release engineering team to support Mozilla-specific task-superseding
  needs and hosted outside of the Taskcluster installation. On the other hand,
  [taskcluster-stats-collector](http://github.com/taskcluster/taskcluster-stats-collector)
  is deployed within the Firefox Taskcluster deployment, but is
  Firefox-specific and not part of a public Taskcluster release.

* While a Taskcluster release will likely encompass some pre-built worker
  images for various cloud platforms, sophisticated worker deployment is the
  responsibility of individual users. That may mean deploying workers to
  hardware where necessary, perhaps with modifications to the build
  configurations or even entirely custom-built worker implementations.  We will
  provide cloud-provisioning tools that can be used to dynamically instantiate
  user-specified images.

#### Generated Client Libraries

The second point above raises an interesting quandry: Taskcluster uses code
generation to create its API client libraries. Historically, we have just
pushed the "latest" client to the [package
repository](https://yarnpkg.com/en/package/taskcluster-client) and carefully
choreographed any incompatible changes. For users who have not customized their
deployment, this is not too much trouble: any release of Taskcluster will have
a client library in the package repository corresponding to it.  We don't have
a great way to indicate which version that is, but perhaps we will invent
something.

But when Taskcluster installations are customized by adding additional
services, progress is no longer linear: each user has a distinct "fork" of the
Taskcluster API surface containing the locally-defined services. Development of
Taskcluster components poses a similar challenge: if I add a new API method to
a service, how do I call that method from another service without pushing a new
library to the package repository?

The question is further complicated by the use of compiled languages. While
Python and JS clients can simply load a schema reference file at runtime (for
example, a file generated at deploy time), the Go and Java clients "bake in"
the references at compile time.

Despite [much discussion](https://bugzilla.mozilla.org/show_bug.cgi?id=1428417),
we have yet to settle on a good solution for this issue.

### Everything is Public!

Mozilla is Open by Design, and so is Taskcluster: with the exception of data
that must remain private (passwords, encryption keys, and material covered by
other companies' NDAs), everything is publicly accessible. We take advantage of
that by reading data without any authentication. For example, the [action
specification](https://docs.taskcluster.net/manual/using/actions/spec)
describes downloading a decision task's `public/action.json` artifact. Nowhere
does it mention providing any credentials to fetch the decision task, nor to
fetch the artifact itself.

This is a rather fundamental design decision, and changing it would be
difficult. We might embark on that process, but we might also declare
Taskcluster an open-by-design system, and require non-OSS users to invent other
methods of hiding their data, such as firewalls and VPNs.

### Transitioning from taskcluster.net

Firefox build, test, and release processes run at massive scale on the existing
Taskcluster instance at https://taskcluster.net, along with a number of smaller
Mozilla-associated projects. As we work on this "redeployability" project, we
must continue to deploy from master to that service as well -- the rootUrl
special-case mentioned above is a critical part of this compatibility. We will
not be running either new or old instances from long-living Git branches.

Some day, we will need to move all of these projects to a newly redeployed
cluster and delete the old. That day is still in the distant future. It will
likely involve some running of tasks in parallel to expunge any leftover
references to `taskcluster.net`, then a planned downtime to migrate everything
over (we will want to maintain task and artifact history, for example). We will
likely finish up by redeploying a bunch of permanent redirects from
`taskcluster.net` domains.

# Conclusion

That's just a short list of some of the challenges we face in transmuting a
hosted service into a shipped application.

All the while, of course, we must "keep the lights on" for the existing
deployment, and continue to meet Firefox's needs. At the moment that includes a
project to deploy Taskcluster workers on arm64 hardware in https://packet.net,
development of the docker-engine to replace the aging [docker
worker](https://github.com/taskcluster/docker-worker), using [hooks for
actions](https://bugzilla.mozilla.org/show_bug.cgi?id=1415868) to reduce the
scopes afforded to level-3 users, improving taskcluster-github to support
defining decision tasks, and the usual assortment of contributed pull requests,
issue debugging, service requests.
