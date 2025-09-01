import http from 'k6/http';

import { sleep } from 'k6';

export const options = {
  // Define the number of iterations for the test
  iterations: 20,
  // Define the numer of virtual users
  vus: 4
};


export default function () {
  http.get('http://localhost:8082');

  sleep(1);
}
