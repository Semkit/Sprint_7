import requests
import allure
from task import register_new_courier_and_return_login_password
from task import generate_random_string
from task import URL


class TestLogin:

    @allure.title("Проверка авторизации курьера")
    def test_courier_login(self):
        with allure.step("Создание нового курьера"):
            login_pass = register_new_courier_and_return_login_password()
            login, password, _ = login_pass

        with allure.step("Авторизация созданного курьера"):
            payload = {
                "login": login,
                "password": password
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
            assert "id" in response.json(), f"Ожидался 'id' в ответе, но получен {response.json()}"

    @allure.title("Проверка обязательных полей при авторизации курьера")
    def test_courier_login_missing_fields(self):
        fields = ["login", "password"]

        for field in fields:
            with allure.step(f"Проверка без поля {field}"):
                payload = {
                    "login": generate_random_string(10) if field != "login" else "",
                    "password": generate_random_string(10) if field != "password" else ""
                }
                payload = {k: v for k, v in payload.items() if v is not None}
                response = requests.post(f'{URL}/courier/login', json=payload)
                assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
                assert response.json()["message"] == "Недостаточно данных для входа", f"Ожидалось сообщение 'Недостаточно данных для входа', но получено {response.json()['message']}"

    @allure.title("Проверка авторизации с неверным логином или паролем")
    def test_courier_login_invalid_credentials(self):
        with allure.step("Создание нового курьера"):
            login_pass = register_new_courier_and_return_login_password()
            login, password, _ = login_pass

        with allure.step("Авторизация с неверным логином"):
            payload = {
                "login": generate_random_string(10),
                "password": password
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Ожидалось сообщение 'Учетная запись не найдена', но получено {response.json()['message']}"

        with allure.step("Авторизация с неверным паролем"):
            payload = {
                "login": login,
                "password": generate_random_string(10)
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Ожидалось сообщение 'Учетная запись не найдена', но получено {response.json()['message']}"

    @allure.title("Проверка авторизации несуществующего пользователя")
    def test_courier_login_nonexistent_user(self):
        with allure.step("Авторизация с несуществующим пользователем"):
            payload = {
                "login": generate_random_string(10),
                "password": generate_random_string(10)
            }
            response = requests.post(f'{URL}/courier/login', json=payload)

            assert response.status_code == 404, f"Ожидался статус 404, но получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Ожидалось сообщение 'Учетная запись не найдена', но получено {response.json()['message']}"


