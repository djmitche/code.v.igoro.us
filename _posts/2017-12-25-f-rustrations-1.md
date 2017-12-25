---
title: FRustrations 1
layout: post
date:   2017-12-25 15:00:00
categories: [mozilla,rust]
---

## Foreword

I've been hacking about learing Rust for a bit more than a year now, building a [Hawk](https://crates.io/crates/hawk) crate and hacking on a distributed lock service named [Rubbish](https://github.com/djmitche/rubbish) (which will never amount to anything but gives me a purpose).

In the process, I've run into some limits of the language.
I'm going to describe some of those in a series of posts starting with this one.

One of the general themes I've noticed is lots of things work great in demos, where everything is in a single function (thus allowing lots of type inference) and most variables are `'static`.
Try to elaborate these demos out into a working application, and the borrow checker immediately blocks your path.

Today's frustration is a good example.

# Ownership As Exclusion and Async Rust

A common pattern in Rust is to take ownership of a resource as a way of excluding other uses until the operation is finished.
In particular, the [send](https://docs.rs/futures/0.1.17/futures/sink/trait.Sink.html#method.send) method of Sinks in the futures crate takes `self`, not `&self`.
Because this is an async function, its result is a [future that will yield the Sink on success](https://docs.rs/futures/0.1.17/futures/sink/struct.Send.html#impl-Future).

The safety guarantee here is that only one async `send` can be performed at any given time.
The language guarantees that nothing else can access the Sink until the `send` is complete.

## Building a Chat Application

As part of learning about Tokio, Futures, and so on, I elected to build a chat application, starting with the [simple pipelined server](https://tokio.rs/docs/getting-started/pipeline-server/) in the Tokio docs.
This example uses `Stream::and_then` to map requests to responses, which makes sense for a strict request/response protocol, but does not make sense for a chat protocol.
It should be possible to send or receive a message at any time in a chat protocol, so I modified the example to use `send` to send one message at a time:

```
    let server = connections.for_each(move |(socket, _peer_addr)| {
        let (writer, _reader) = socket.framed(LineCodec).split();

        let server = writer.send("Hello, World!".to_string())
            .and_then(|writer2| writer2.send("Welcome to Chat.".to_string())
            .then(|_| Ok(()));
        handle.spawn(server);

        Ok(())
    });
```

This bit works fine: the resulting server greets each user, then drops the socket and disconnects them, as expected.
Note the threading of the writer: the first `writer.send` is using the writer returned from `split`, while the second is using the result of the Future from the first (I have unecessarily called it `writer2` here for clarity).
In fact, `send` moves `self`, so `writer.send("Welcome to Chat".to_string())` would not be permitted as that value has been moved.

Based on how I would design a chat app in Python, JavaScript, or any other language, I chose to make a struct to represent a connected user in the chat:

```
pub struct ChatConnection {
    reader: SplitStream<Framed<TcpStream, LineCodec>>,
    writer: SplitSink<Framed<TcpStream, LineCodec>>,
    peer: SocketAddr,
}

impl ChatConnection {
    fn new(socket: TcpStream, peer: SocketAddr) -> ChatConnection {
        let (writer, reader) = socket.framed(LineCodec).split();
        ChatConnection {
            writer: writer,
            reader: reader,
            peer: peer,
        }   
    }   

    fn run(&self) -> Box<Future<Item = (), Error = ()>> {
        Box::new(self.writer
            .send("Welcome to Chat!".to_string())
            .then(|_| Ok(())))
    }   
}
```

When a new connection arrives, other code allocates a new `ChatConnection` and calls its `run` method, spawning a task into the event loop with the resulting future.

This doesn't work, though:

```
error[E0507]: cannot move out of borrowed content
  --> src/main.rs:82:18
   |
   |         Box::new(self.writer
   |                  ^^^^ cannot move out of borrowed content
```

There's sense in this: the language is preventing multiple simultaneous sends.
If it allowed `self.writer` to be accessible to other code while the Future was not complete, then that other code could potentially, unsafely, call `send` again.

But it makes it difficult to store the writer in a struct -- something any reasonably complex application is going to need to do.
The two Rust-approved solutions here are to always move `writer` around as a local variable (as done in the demo), or to move `self` in the `run` method (`fn run(self) ..`).
The first "hides" `writer` in a thicket of closures, making it difficult or impossible to find when, for example, another user sends this one a private message.
The second just moves the problem: now we have a `ChatConnection` object to which nothing but the `run` method is allowed to refer, meaning that nothing can communicate with it.

## The Fix

The most obvious fix is to wrap the `writer` in another layer of abstraction with runtime safety guarantees.
This means something like a `Mutex`, although the `Mutex` class will block a thread on conflict, which will result in deadlock in a single-threaded, asynchronous situation such as this one.
I assume there is some Futures equivalent to `Mutex` that will return a `Future<Item = Guard>` which resolves when the underlying resource is available.

Looking at some of the existing [chat](https://github.com/jgallagher/tokio-chat-example/blob/master/tokio-chat-server/src/main.rs) [examples](https://github.com/tokio-rs/tokio-core/blob/master/examples/chat.rs), I see that they use ``futures::sync::mpsc`` channels to communciate between connections.
This is in keeping with the stream/sink model (channels are just another form of a stream), but replacing the Future-yielding `send` with the non-blocking (but memory-unbounded) `unbounded_send` method.

## Frustration

I feel like this solution is "cheating": the language makes it difficult to send messages on the channel it provides, so wrap it in anohter channel with better semantics.
Even the code to connect those two channels is, to my eye, obfuscating this issue:

```
        let socket_writer = rx.fold(writer, |writer, msg| {
            let amt = io::write_all(writer, msg.into_bytes());
            let amt = amt.map(|(writer, _)| writer);
            amt.map_err(|_| ())
        });
```

That `rx.fold` function is doing a lot of work, but there is nary a comment to draw attention to this fact.
Those accustomed to functional programming, and familiar with Rust's use of the term "fold" for what most languages call "reduce", might figure out what's going on more quickly.
The `writer` is moved into the accumulator for the fold (reduce) operation, then moved into the closure argument, and when the future is finished it is moved back into the accumulator for the next iteration.
This is a clever application of the first Rust-approved solution above: move the `writer` around in local variables without ever landing it in a stable storage location.

So, this is a key characteristic of asynchronous Rust, without which programs will not compile.
Yet these "examples", which are meant to be instructive, bury the approach behind some clever stream combinators as if they are ashamed of it.
The result is almost immediate frustration and confusion for the newcomer to asynchronous Rust trying to learn from these examples.
