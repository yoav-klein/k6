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
    // define scenarios
        breaking: {
            executor: 'ramping-vus',
            stages: [
                { duration: '10s', target: 20 },
                { duration: '50s', target: 100 },
                { duration: '50s', target: 500 },
                { duration: '50s', target: 1000 },
                { duration: '50s', target: 2000 },
            ]
        },
    },
}

export default function () {
  // define URL and payload
  const url = 'https://quickpizza.grafana.com/api/users/token/login';
  const payload = JSON.stringify({
    username: 'default',
    password: '1234',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // send a post request and save response as a variable
  const res = http.post(url, payload, params);

  // add a check to check the response status code
  check(res, {
    'response code was 200': (res) => res.status == 200,
  });
}
