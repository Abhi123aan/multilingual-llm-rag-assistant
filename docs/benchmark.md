# Benchmark Notes

No repeatable load test has been run for this repository yet.

The README intentionally avoids unverified claims such as "2-5 second response time" or "supports multiple simultaneous users" until a Locust or k6 run is checked in with environment details and raw results.

Suggested benchmark command once the API is running locally:

```bash
locust -f scripts/locustfile.py --host http://localhost:8000
```
