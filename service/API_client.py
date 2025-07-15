from abc import ABC, abstractmethod
from urllib.parse import urljoin
import requests

class IHTTPClient(ABC):
    @abstractmethod
    def get(self, url: str, params: dict) -> dict:
        pass

class RequestsClient(IHTTPClient):
    def get(self, url: str, params: dict) -> dict:
        response = requests.get(url, params=params, timeout=600)
        response.raise_for_status()
        return response.json()

class APIClient:
    def __init__(self, base_url: str, http_client: IHTTPClient):
        self.base_url = base_url.rstrip('/') + '/'
        self.http_client = http_client

    def translate_to_morse(self, text: str) -> str:
        """Перевод текста в азбуку Морзе"""
        endpoint = "translator/morse/to_morse"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"text": text}
        )
        return result["translated_text"]

    def translate_from_morse(self, text: str) -> str:
        """Декодирование азбуки Морзе в текст"""
        endpoint = "translator/morse/from_morse"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"text": text}
        )
        return result["translated_text"]

    def translate_keyboard(self, text: str, direction: str) -> str:
        """Конвертация раскладки клавиатуры"""
        endpoint = "translator/keyboard/keyboard"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"text": text, "direction": direction}
        )
        return result["translated_text"]

    def generate_password(self, length: str) -> str:
        """Генерация пароля"""
        endpoint = "password_manager/generator/generate"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"length": length}
        )
        return result["password"]

    def check_password(self, password: str) -> dict:
        """Проверка сложности пароля"""
        endpoint = "password_manager/checker/check"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"password": password}
        )
        return {"score": result["score"], "problems": result["problems"]}

    def convert_bases(self, from_base: str, to_base: str, number: str) -> str:
        """Конвертация между системами счисления"""
        endpoint = "converter/bases/convert"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"from_base": from_base, "to_base": to_base, "number": number}
        )
        return result["converted_number"]

    def convert_to_roman(self, number: str) -> str:
        """Арабские → Римские цифры"""
        endpoint = "converter/roman/to_roman"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"number": number}
        )
        return result["converted_text"]

    def convert_from_roman(self, number: str) -> str:
        """Римские → Арабские цифры"""
        endpoint = "converter/roman/from_roman"
        result = self.http_client.get(
            urljoin(self.base_url, endpoint),
            params={"number": number}
        )
        return result["converted_text"]
