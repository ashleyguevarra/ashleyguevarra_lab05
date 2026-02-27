"""
Locustfile for load testing store_manager.py
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import random
from locust import HttpUser, task, between

class FlaskAPIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Called every time a Locust user spawns"""
        print("User started test session")

    @task(3)
    def create_order(self):
        """Load test for order creation"""
        payload = {
            "user_id": random.randint(1, 3),
            "items": [
                {
                    "product_id": random.randint(1, 4),
                    "quantity": random.randint(1, 10)
                }
            ]
        }

        with self.client.post(
            "/store-manager-api/orders",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code != 201:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                response.success()

    @task(0)
    def test_rate_limit(self):
        """Test pour vérifier le rate limiting (désactivé pour Q7)"""
        payload = {
            "user_id": random.randint(1, 3),
            "items": [
                {
                    "product_id": random.randint(1, 4),
                    "quantity": random.randint(1, 10)
                }
            ]
        }

        with self.client.post(
            "/store-manager-api/orders",
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 503:
                response.failure("Rate limit atteint (503)")
            elif response.status_code != 201:
                response.failure(f"Unexpected status: {response.status_code}")
            else:
                response.success()