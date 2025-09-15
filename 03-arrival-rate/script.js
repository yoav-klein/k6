// import necessary module
import http from 'k6/http';
import { check } from 'k6';

export const options = {
    // define thresholds
    thresholds: {
        http_req_failed: ['rate<0.01'], // error rate less than 1%
        http_req_duration: ['p(99)<1000'] // 99% of request should take less than 1 second
    },
    scenarios: {
    // arbitrary name of scenario
      average_load: {
        executor: 'constant-arrival-rate',
        duration: '20s',
        rate: 300,
        timeUnit: "1s",
        preAllocatedVus: 100
    },
  },
}

export default function () {
  // define URL and payload
  const url = 'http://localhost:8090/api/delay/500';

  // send a post request and save response as a variable
  const res = http.get(url);

  // add a check to check the response status code
  check(res, {
    'response code was 200': (res) => res.status == 200,
  });
}
