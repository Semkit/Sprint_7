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
            assert login_pass, "Registration failed, login_pass is empty"
            login, password, _ = login_pass

        with allure.step("Авторизация созданного курьера"):
            payload = {
                "login": login,
                "password": password
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
            assert "id" in response.json(), f"Expected 'id' in response, but got {response.json()}"

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
                assert response.status_code == 400, f"Expected 400, but got {response.status_code}"
                assert response.json()["message"] == "Недостаточно данных для входа", f"Expected 'Недостаточно данных для входа', but got {response.json()['message']}"

    @allure.title("Проверка авторизации с неверным логином или паролем")
    def test_courier_login_invalid_credentials(self):
        with allure.step("Создание нового курьера"):
            login_pass = register_new_courier_and_return_login_password()
            assert login_pass, "Registration failed, login_pass is empty"
            login, password, _ = login_pass

        with allure.step("Авторизация с неверным логином"):
            payload = {
                "login": generate_random_string(10),
                "password": password
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Expected 'Учетная запись не найдена', but got {response.json()['message']}"

        with allure.step("Авторизация с неверным паролем"):
            payload = {
                "login": login,
                "password": generate_random_string(10)
            }
            response = requests.post(f'{URL}/courier/login', json=payload)
            assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Expected 'Учетная запись не найдена', but got {response.json()['message']}"

    @allure.title("Проверка авторизации несуществующего пользователя")
    def test_courier_login_nonexistent_user(self):
        with allure.step("Авторизация с несуществующим пользователем"):
            payload = {
                "login": generate_random_string(10),
                "password": generate_random_string(10)
            }
            response = requests.post(f'{URL}/courier/login', json=payload)

            assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена", f"Expected 'Учетная запись не найдена', but got {response.json()['message']}"


