import http from 'k6/http';
import { check } from 'k6';

export const options = {
    vus: 20,
    duration: '30s',
    thresholds: {
        checks: ['rate>0.93'],
        http_req_duration: ['p(99)<500', 'p(90)<400']
    }
};

export default function() {
    let res = http.get('http://localhost:5000/api/delay/random');
    check(res, {
        'check status is 200': (res) => res.status === 200
    });

}
