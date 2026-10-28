# Atomic notes: data structures

Source: supplied classroom fragments. Each section below is one atomic note.

## Stack

A stack removes the most recently added item first: **last in, first out (LIFO)**.
`push` adds an item at the top; `pop` removes an item from the top. An undo history
can use a stack.

Related: [Removal order and storage](#removal-order-and-storage) distinguishes
this removal rule from a storage layout.

## Queue

A queue removes the earliest added item first: **first in, first out (FIFO)**.
`enqueue` adds an item at the rear; `dequeue` removes an item from the front.
A queue can hold tasks waiting for service.

Related: [Removal order and storage](#removal-order-and-storage) distinguishes
this removal rule from a storage layout.

## Removal order and storage

LIFO and FIFO describe the order in which items are removed; they do not specify
a storage layout. The source gives no operation time complexities.

Related: [Stack](#stack) uses LIFO; [Queue](#queue) uses FIFO. These links compare
the two removal rules described in the source.

Suggested connection: the mentioned `performance.md` could discuss operation
costs, but its contents and target are unavailable here. It has not been linked
or used as evidence.
