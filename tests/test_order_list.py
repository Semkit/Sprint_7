import requests
import allure
from task import URL


class TestOrderList:
    @allure.title("Проверка получения списка заказов")
    def test_get_orders_list(self):
        with allure.step("Отправка запроса для получения списка заказов"):
            response = requests.get(f'{URL}/orders')
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
