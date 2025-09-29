import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 200,
  duration: '30s',
};

export default function() {
    let res = http.get('http://localhost:5000/api/random_fail');
    check(res, {
        'check status is 200': (res) => res.status === 200
    });
}
