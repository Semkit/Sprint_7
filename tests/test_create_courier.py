import requests
import allure
from task import generate_random_string
from task import register_new_courier_and_return_login_password
from task import URL


class TestCouriers:

    @allure.title("Проверка создания курьера")
    def test_create_courier(self):
        with allure.step("Создание нового курьера"):
            login_pass = register_new_courier_and_return_login_password()
            assert len(login_pass) == 3, f"Ожидалось три элемента данных для курьера, но получено {len(login_pass)}"


    @allure.title("Проверка невозможности создания двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        with allure.step("Создание нового курьера"):
            login_pass = register_new_courier_and_return_login_password()

            login, password, first_name = login_pass
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        with allure.step("Создание курьера с тем же логином"):
            response = requests.post(f'{URL}/courier', json=payload)
            assert response.status_code == 409, f"Ожидался статус 409, но получен {response.status_code}"
            assert response.json()[
                       "message"] == "Этот логин уже используется. Попробуйте другой.", f"Ожидался статус 'Этот логин уже используется', но получен {response.json()['message']}"


    @allure.title("Проверка обязательных полей при создании курьера")
    def test_create_courier_with_missing_fields(self):

        fields = ["login", "password"]#, "firstName"]
        base_payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        for field in fields:
            with allure.step(f"Проверка без поля {field}"):
                payload = {k: v for k, v in base_payload.items() if k != field}
                response = requests.post(f'{URL}/courier', json=payload)
                assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
                assert response.json()["message"] == "Недостаточно данных для создания учетной записи", f"Ожидалось сообщение 'Недостаточно данных для создания учетной записи', но получено {response.json()['message']}"
