# Thresholds
---

You can use thresholds to define the success and fail criteria of your tests.
Thresholds are a set of tests that compare a certain metric to predefined values.

In this example, we define a threshold that `p(90)` of our HTTP requests need to be below 400ms (which will pass)
and anohter one that `p(99)` needs to be below 500ms (which will fail)

Also, you can combine checks and thresholds to define that a certain number of checks are passed.

## Run

Run the `http-server` application in the `utility-applications` directory.
The `/api/delay/random` endpoint randomly delays a request for a "long" period. You can configure the 
percentage of the delayed requests, and the period. By default its 5% of requests delayed for 500ms.

So in the default configuration, p(90) should be the regular latency of between 1-100ms, and p(95) should be around 500.
So p(99) is clearly above 500.

Then run the tests

You'll see that you'll get the thresholds that failed/passed:
```
  █ THRESHOLDS

    checks
    ✓ 'rate>0.93' rate=100.00%

    http_req_duration
    ✗ 'p(99)<500' p(99)=545.75ms
    ✓ 'p(90)<400' p(90)=140.11ms


```
