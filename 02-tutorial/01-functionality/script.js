// import necessary module
import http from 'k6/http';
import { check } from 'k6';


export default function () {
  // define URL and payload
  const url = 'https://quickpizza.grafana.com/api/users/token/login';
  const payload = JSON.stringify({
    username: 'default',
    password: '12345678',
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
