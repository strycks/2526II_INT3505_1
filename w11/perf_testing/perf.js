import http from 'k6/http';
import { check, sleep } from 'k6';

// k6 run perf.js 

export const options = {
    vus: 50,           // concurrent users
    duration: '5s',  
    thresholds: {
        http_req_duration: ['p(95)<200'],  // ms
        http_req_failed: ['rate<0.01'],   
    },
};

export default function () {
    const url = 'http://localhost:5000/api/v1/books'; 
    const jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3Njk2NDU4OSwianRpIjoiYWQ5NjY2MjktYjA5NC00NTAzLWE3MzMtMjkzNWNmODc2ZDc0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzc2OTY0NTg5LCJjc3JmIjoiN2U4MDU4MDktODRkNC00MThmLWFiY2YtZWVmNmExODdlNzczIiwiZXhwIjoxNzc2OTY1NDg5LCJyb2xlIjoiYWRtaW4ifQ.gibOfB101pqZqXcN4BeLXSEwYVa-6G8CBKOm_bf1NA4'
    
    const params = { headers: { 'Authorization': 'Bearer ' + jwt } };
    const res = http.get(url, params);

    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    // sleep 0.5s after each response
    sleep(0.5); 
}