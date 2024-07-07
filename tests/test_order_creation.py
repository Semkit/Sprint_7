import requests
import allure
import pytest
from task import URL


class TestOrder:

    def generate_order_payload(self, colors):
        return {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": colors
        }

    @allure.title("Проверка создания заказа")
    @pytest.mark.parametrize("colors", [
        (["BLACK"]),
        (["GREY"]),
        (["BLACK", "GREY"]),
        ([])
    ])
    def test_create_order(self, colors):
        order = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": colors
        }

        with allure.step(f"Создание заказа с цветами: {colors}"):
            response = requests.post(f'{URL}/orders', json=order)
            assert response.status_code == 201, f"Expected 201, but got {response.status_code}"
            response_json = response.json()
            assert "track" in response_json, f"Expected 'track' in response, but got {response_json}"
