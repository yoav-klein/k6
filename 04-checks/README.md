# Checks
---

The `check` function allows you to validate the results of the system under test.

In this simple example we check if the HTTP GET call was responded with status code 200.

## Run

Run the `http-server` application in the `utility-applications` directory.
The `/api/random_fail` endpoint randomly returns 404 instead of 200. The percentage 
of failed responses may be customized with env vars.

Then run the test.

You'll see that you'll get the statistics of how many checks passed/failed:
```

  █ TOTAL RESULTS

    checks_total.......: 8661   160.707835/s
    checks_succeeded...: 95.25% 8250 out of 8661
    checks_failed......: 4.74%  411 out of 8661

    ✗ check status is 200
      ↳  95% — ✓ 8250 / ✗ 411

```
