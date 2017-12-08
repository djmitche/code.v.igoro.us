---
title: Parameterized Roles
layout: post
date:   2017-12-08 15:00:00
categories: [mozilla,taskcluster]
---

The [roles](https://docs.taskcluster.net/reference/platform/taskcluster-auth/docs/roles) functionality in Taskcluster is a kind of "macro expansion": given the roles

<pre>
group:admins -> admin-scope-1
                admin-scope-2
                assume:group:devs
group:devs   -> dev-scope
</pre>

the scopeset `["assume:group:admins", "my-scope"]` expands to

<pre>
[
    "admin-scope-1",
    "admin-scope-2",
    "assume:group:admins",
    "assume:group:devs",
    "dev-scope",
    "my-scope",
]
</pre>

because the `assume:group:admins` expanded the `group:admins` role, and that recursively expanded the `group:devs` role.

However, this macro expansion did not allow any parameters, similar to allowing function calls but without any arguments.

The result is that we have a lot of roles that look the same.
For example, [project-admin:..](https://tools.taskcluster.net/auth/roles/project-admin%3Afocus) roles all have similar scopes (with the project name included in them), and a big warning in the description saying "DO NOT EDIT".

# Role Parameters

Now we can do better!
A role's scopes can now include `<..>`.
When expanding, this string is replaced by the portion of the scope that matched the `*` in the roleId.
An example makes this clear:

<pre>
project-admin:* -> assume:hook-id:project-<..>/*
                   assume:project:<..>:*
                   auth:create-client:project/<..>/*
                   auth:create-role:hook-id:project-<..>/*
                   auth:create-role:project:<..>:*
                   auth:delete-client:project/<..>/*
                   auth:delete-role:hook-id:project-<..>/*
                   auth:delete-role:project:<..>:*
                   auth:disable-client:project/<..>/*
                   auth:enable-client:project/<..>/*
                   auth:reset-access-token:project/<..>/*
                   auth:update-client:project/<..>/*
                   auth:update-role:hook-id:project-<..>/*
                   auth:update-role:project:<..>:*
                   hooks:modify-hook:project-<..>/*
                   hooks:trigger-hook:project-<..>/*
                   index:insert-task:project.<..>.*
                   project:<..>:*
                   queue:get-artifact:project/<..>/*
                   queue:route:index.project.<..>.*
                   secrets:get:project/<..>/*
                   secrets:set:project/<..>/*
</pre>

With the above *parameterized* role in place, we can delete all of the existing
`project-admin:..` roles: this one will do the job.
A client that has `assume:project-admin:bugzilla` in its scopes will have `assume:hook-id:project:bugzilla/*` and all the rest in its expandedScopes.

There's one caveat: a client with `assume:project-admin:nss*` will have `assume:hook-id:project:nss*` -- note the loss of the trailing `/`.
The `*` consumes any parts of the scope after the `<..>`.
In practice, as in this case, this is not an issue, but could certainly cause surprise for the unwary.

# Implementation

Parameterized roles seem pretty simple, but they're not!

## Efficiency

Before parameterized roles the Taskcluster-Auth service would pre-compute the full expansion of every role.
That meant that any API call requiring expansion of a set of scopes only needed to combine the expansion of each scope in the set -- a linear operation.
This avoided a (potentially exponential-time!) recursive expansion, trading some up-front time pre-computing for a faster response to API calls.

With parameterized roles, such pre-computation is not possible.
Depending on the parameter value, the expansion of a role may or may not match other roles.
Continuing the example above, the role `assume:project:focus:xyz` would be expanded when the parameter is `focus`, but not when the parameter is `bugzilla`.

The fix was to implement the recursive approach, but in such a way that non-pathological cases have reasonable performance.
We use a [trie](https://github.com/taskcluster/taskcluster-auth/blob/master/src/trie.js) which, given a scope, returns the set of scopes from any matching roles along with the position at which those scopes matched a `*` in the roleId.
In principle, then, we resolve a scopeset by using this trie to expand (by one level) each of the scopes in the scopeset, substituting parameters as necessary, and recursively expand the resulting scopes.

To resolve a scope set, we [use a queue to "flatten" the recursion, and keep track of the accumulated scopes as we proceed](https://github.com/taskcluster/taskcluster-auth/blob/ac1c904f840c4703a27f43a189725b4a7e986b04/src/scoperesolver.js#L320-L394).
We already had some [utility functions](https://github.com/taskcluster/taskcluster-lib-scopes) that allow us to make a few key optimizations.
First, it's only necessary to expand scopes that start with `assume:` (or, for completeness, things like `*` or `assu*`).
More importantly, if a scope is already included in the `seen` scopeset, then we need not enqueue it for recursion -- it has already been accounted for.

In the end, the new implementation is tens of milliseconds slower for some of the more common queries.
While not ideal, in practice that as not been problematic.
If necessary, some simple caching might be added, as many expansions repeat exactly.

## Loops

An advantage of the pre-computation was that it could seek a "fixed point" where further expansion does not change the set of expanded scopes.
This allowed roles to refer to one another:

<pre>
some-role -> assume:another-role
another*  -> assume:some-role
</pre>

A naïve recursive resolver might loop forever on such an input, but could easily track already-seen scopes and avoid recursing on them again.
The situation is much worse with parameterized roles.
Consider:

<pre>
some-role-*    -> assume:another-role-<..>x
another-role-* -> assume:some-role-<..>y
</pre>

A simple recursive expansion of `assume:some-role-abc` would result in an infinite set of roles:

<pre>
assume:another-role-abcx
assume:some-role-abcxy
assume:another-role-abcxyx
assume:some-role-abcxyxy
...
</pre>

We forbid such constructions using a [cycle check](https://github.com/taskcluster/taskcluster-auth/blob/ac1c904f840c4703a27f43a189725b4a7e986b04/src/scoperesolver.js#L232-L302), configured to reject only cycles that involve parameters.
That permits the former example while prohibiting the latter.

## Atomic Modifications

But even that is not enough!
The existing implementation of roles stored each role in a row in [Azure Table Storage](https://azure.microsoft.com/en-us/services/storage/tables/).
Azure provides concurrent access to and modification of rows in this storage, so it's conceivable that two roles which together form a cycle could be added simultaneously.
Cycle checks for each row insertion would each see only one of the rows, but the result after both insertions would cause a cycle.
Cycles will crash the Taskcluster-Auth service, which will bring down the rest of Taskcluster.
Then a lot of people will have a bad day.

To fix this, we moved roles to [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/), putting all roles in a single blob.
This service uses ETags to implement atomic modifications, so we can [perform a cycle check before committing](https://github.com/taskcluster/taskcluster-auth/blob/ac1c904f840c4703a27f43a189725b4a7e986b04/src/v1.js#L691-L732) and be sure that no cyclical configuration is stored.

# What's Next

The parameterized role support is running in production now, but we have no yet updated any roles, aside from a few test roles, to use it.
The next steps are to use the support to address a few known weak points in role configuration, including the project administration roles used as an example above.
