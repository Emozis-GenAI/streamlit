import requests 
import json

from core.logger import logger
from core.config import configs

class LoginService:
    @staticmethod
    def register_api(data):
        response = requests.post(
            url=f"{configs.API_URL}/user/register",
            json=data
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                logger.success(response_json["message"])

                return True
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")

        return False

    @staticmethod
    def login_api(data):
        response = requests.post(
            url=f"{configs.API_URL}/user/login",
            json=data
        )
        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "success":
                logger.success(response_json["message"])

                return response_json["data"]
            else:
                logger.warning(response_json["message"])
        else:
            logger.warning("🚨 API 연결에 실패했습니다.")

        return None