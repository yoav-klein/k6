
# Performance
---

After defining the functionality of our tests, now let's start applying load to see how our system behaves under load.

We start with a simple `--iterations` run, where we just tell k6 to run the test this many times.
Then, we proceed to a more advanced use case by introducing the `scenarios` option in the `options` object.

