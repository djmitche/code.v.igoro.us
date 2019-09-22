# Short Variable Declarations Are (Almost) Redundant

The `:=` keyword is referred to as short variable declaration.
It is governed by some [complex rules](https://golang.org/ref/spec#Short_variable_declarations) that dictate when it can and cannot be used.

In practice, as I am modifying code, this generates a lot of noise.
For example, given a function

```go
func doThings() error {
	x, err := thing1();
	if err != nil {
		return err
	}

	err = thing2(x);
	if err != nil {
		return err
	}

	// ...
}
```

If this function is modified to remove the call to `thing1`, the `=` in the call to `thing2` must be changed to `:=`.
This is all the more annoying when doing something temporary like commenting out the call to `thing1` for a moment.
In practice, I just add and remove `:` as the compiler instructs me until the code compiles.

Which means, the compiler can infer which form is correct in most cases.
Could it do so in all cases?
If so, could the language drop the construct or set up `gofmt` to automatically add or remove `:` as necessary?

## The Rules

Well, not quite.
[Inanc Gumus](https://blog.learngoprogramming.com/golang-short-variable-declaration-rules-6df88c881ee) has a nice summary of the rules:

**You can't use it twice for the same variable**

```go
legal := 42
legal ?? 43
```

The `??` here must unambiguously be `=`.

**You can use them twice in multi-variable declarations(\*)** and **You can use them for multi-variable declarations and assignments**

```go
foo, bar := someFunc()
foo, bing ?? someFunc()
bar, bing ?? someFunc()
```

Again, the first `??` is completely specified: it must be `:=` because `bing` is new.
The second is also clear: it must be `=` because neither variable is new.

**You can use them if a variable is already declared with the same name before** and **You can reuse them in scoped statement contexts like if, for, switch**

```go
var foo int = 34

func someFunc() {
	foo ?? 42
	// ...
}
```

This example is ambiguous.
If `??` is replaced with `=`, then `someFunc` will modify the global `foo`.
If `??` is replaced with `:=`, then `foo` is a local variable that [shadows](https://en.wikipedia.org/wiki/Variable_shadowing) the global `foo`, and the global will not be modified.

```go
foo := 34

if foo ?? aFunction(); foo == 34 {
	// ...
}
```

The situation is the same here: depending on the presence of those two little dots `:`, this will either modify or shadow the global `foo`.

## Shadowing

Shadowing is bad.
Programmers shouldn't be allowed to do it.

I can see counter-arguments, sure, but Golang's got a habit of making sweeping statements and enforcing them with the compiler, so why not here?
It makes sense from a safety perspective, too: languages shouldn't allow programmers to do the sort of things that get programmers in trouble.
That's the elevator pitch for Rust!

Here's a particularly insidious case:

```go
var foo int = 34

func someFunc() {
	foo, bar := 42, 43
}
```

Do you know what that `:=` does with `foo`?
Are you sure?
If the correctness of a patch depended on the distinction, would you catch it in review?

The answer is that it makes a new local `foo` that shadows the global.
I expect this is why the [language spec](https://golang.org/ref/spec#Short_variable_declarations) refers to this as "redeclaring" when one of several variables to the left of `:=` is already defined.
That's pretty subtle.

## Suggestion

So, let's have just a single declaration / assignment operator, `=`.
In cases where the variable is already in scope (including in a surrounding scope), it acts as assignment.
In cases where the variable is not defined, it declares the variable.

That means it's impossible to shadow a global variable:

```
var foo int = 34

func someFunc() {
	foo = 42
}
```

This snippet will always and unambgiuously assign to the global variable.
That's easy to remember!

This simplifies writing Go code, and reduces the "churn" of adding and removing `:` throughout a function body as the code develops.

A downside of this approach is that a new global variable could unintentionally "capture" existing local variables.
Imagine that the `var foo` line in the previous example was added *after* `someFunc`'s use of `foo` was written, and in a different file in the same package.
Suddenly a local variable has become global, leading perhaps to race conditions or bizarre behavior of a recursive function.

## Alternative Suggestion

OK, let's keep the `=` and `:=` but teach `gofmt` to pick the right one in all unambiguous cases.
To avoid the ambiguous cases, though, let's prohibit shadowing.

```go
var foo int = 34

func someFunc() {
	foo = 42  // legal (assignment to global)
}
func another() {
	foo := 42 // illegal (shadows global)
}
```

Returning to the imaginary case from the first suggestion, adding a global `var foo` to a package where functions use `foo` as a local variable will now result in a compile error due to the newly-introduced shadowing.

Unfortunately, this approach re-introduces the "churn", as `gofmt` happily adds and removes `:` where necessary.

Furthermore, it doesn't remove all pitfalls for the programmer.
Imagine a global variable `foo` already exists, and the programmer carelessly writes `foo = 10`, assuming `gofmt` will fix it up.
Here `gofmt` can't tell that the programmer intended to create a local variable, as the syntax is a valid assignment to the global.

---

# TODO

:= vs = is entirely specified
multiple incompatible vendoring solutions
not typesafe in practice, with lots of interface{}
no versioning
relies on code generation for most interesting things -> requires complex, hand-built build processes
no way to write foo.field, newvar := .. or = ..
"classes" do not hang together, easy to mix up
capitalization change means grepping is difficult
indentation rules generate spurious diffs
tabs?  it's the 21st century, and kids these days have never seen a typewriter
no agreement on how to represent arbitrary JSON data
confusion between type names and package names
no circular depenencies

