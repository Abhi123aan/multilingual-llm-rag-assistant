from locust import HttpUser, between, task


class RagApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def query(self):
        self.client.post(
            "/v1/query",
            json={"query": "What is machine learning?", "language": "english"},
        )
