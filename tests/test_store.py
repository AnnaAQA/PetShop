import allure
import pytest
import requests
import jsonschema
from schemas.store_schema import STORE_SCHEMA
from schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Store")
class TestStore:

    @allure.title("Создание нового заказа - test 42")
    def test_add_new_store(self):
        with allure.step("Подготовка данных на создание нового заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "shipDate": "2025-04-03T16:44:27.948",
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
            response_clean_data = response_json['shipDate'][:23]

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, STORE_SCHEMA)

        with allure.step("Проверка параметров ответа"):
            assert response_json['id'] == payload['id'], "параметр id не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "параметр petId не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "параметр quantity не совпадает с ожидаемым"
            assert response_clean_data == payload['shipDate'], "параметр shipDate не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "параметр status не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "параметр complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID - test 43")
    def test_get_store_by_id(self, create_store):
        with allure.step("Получение ID нового заказа"):
            store_id = create_store['id']

        with allure.step("Отправка запроса на получение данных о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка соответствия ID нового заказа"):
            assert response.json()['id'] == store_id

    @allure.title("Удаление существующего заказа - test 44")
    def test_delete_existant_store(self, create_store):
        with allure.step("Получение ID нового заказа"):
            store_id = create_store['id']

        with allure.step("Отправка запроса на удаление заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Попытка получить удалённый заказ"):
            response = requests.get(url=f"{BASE_URL}/store/order/{store_id}")

        with allure.step("Проверка статуса ответа по удаленному заказу"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе - test 45")
    def test_get_nonexistant_store(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа 404"):
            assert response.status_code == 404

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Order not found"

    @allure.title("Получение инвентаря магазина - test 46")
    def test_get_inventory(self):
        with allure.step(f"Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, INVENTORY_SCHEMA)

