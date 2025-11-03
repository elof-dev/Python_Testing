from locust import HttpUser, task
""" test file for performance testing.
3 loading tests with max time of 5 seconds (index, book, logout)
2 update tests with max time of 2 seconds (showSummary, purchasePlaces)
"""

class PerformanceTest(HttpUser):
    
    @task
    def index(self):
        response = self.client.get("/")
        assert response.elapsed.total_seconds() < 5
    
    @task
    def showSummary(self):
        response = self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.elapsed.total_seconds() < 2
    
    @task
    def book(self):
        response = self.client.get("/book/Fall Classic")
        assert response.elapsed.total_seconds() < 5
    
    @task
    def purchasePlaces(self):
        response = self.client.post("/purchasePlaces", data={
            "competition": "Fall Classic",
            "places": "2"
        })
        assert response.elapsed.total_seconds() < 2
    
    @task
    def logout(self):
        response = self.client.get("/logout")
        assert response.elapsed.total_seconds() < 5