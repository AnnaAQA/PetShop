import allure
import jsonschema
import requests
from schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistant_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/0000")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet deleted", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistant_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 0000,
                "name": "nonexistant_pet",
                "status": "available"
            }
        response = requests.put(url=f"{BASE_URL}/pet", json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistant_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных на создание нового питомца"):
            payload = {
                "id": 1,
                "name": "Tom",
                "status": "available"
            }
            with allure.step("Отправка запроса на создание питомца"):
                response = requests.post(url=f"{BASE_URL}/pet", json=payload)
                response_json = response.json()

            with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
                jsonschema.validate(response_json, PET_SCHEMA)

            with allure.step("Проверка параметров ответа"):
                assert response_json['id'] == payload['id'], "параметр id не совпадает с ожидаемым"
                assert response_json['name'] == payload['name'], "параметр name не совпадает с ожидаемым"
                assert response_json['status'] == payload['status'], "параметр status не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца с полными данными")
    def test_add_new_pet_with_full_data(self):
        with allure.step("Подготовка данных на создание нового питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [
                    {
                        "id": 0,
                        "name": "string"
                    }
                ],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров ответа"):
            assert response_json['id'] == payload['id'], "параметр id не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "параметр name не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "параметр status не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "параметр category не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "параметр photoUrls не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "параметр tags не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID нового питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса на получение данных о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка соответствия ID питомца"):
            assert response.json()['id'] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_existant_pet(self, create_pet):
        with allure.step("Получение ID нового питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса на обновление имени"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка ответа c обновленным параметром name"):
            assert response.json()['name'] == payload['name']

    @allure.title("Удаление существующего питомца")
    def test_delete_existant_pet(self, create_pet):
        with allure.step("Получение ID нового питомца"):
            pet_id = create_pet['id']

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Попытка получить удалённого питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа по удаленному питомцу"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"
