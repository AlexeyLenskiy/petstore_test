import requests

from configs.constants import BASE_URL


class PetController:
    def create_pet(self, pet_data: dict) -> requests.Response:
        """
        POST /pet endpoiunt
        """
        response = requests.post(f"{BASE_URL}/pet", json=pet_data)
        return response

    def get_pet(self, pet_id) -> requests.Response:
        """
        GET /pet/{petId} endpoiunt
        """
        response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        return response

    def get_pet_by_status(self, status_param: str) -> requests.Response:
        """
        GET /pet/findByStatus endpoiunt
        """
        response = requests.get(f"{BASE_URL}/pet/findByStatus{status_param}")
        return response

    def update_pet(self, pet_data: dict) -> requests.Response:
        """
        PUT /pet endpoiunt
        """
        response = requests.put(f"{BASE_URL}/pet", json=pet_data)
        return response

    def delete_pet(self, pet_id: int) -> requests.Response:
        """
        DELETE /pet/{petId} endpoiunt
        """
        response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
        return response
