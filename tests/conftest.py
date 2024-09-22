import random

import pytest
from faker import Faker

from controllers.pet_controller import PetController
from models.pet import PetBody

api = PetController()
fake = Faker(locale="ru_RU")


@pytest.fixture()
def delete_pets(pet_data: PetBody) -> None:
    pet_id = pet_data.id
    api.delete_pet(pet_id)


@pytest.fixture()
def create_pet(pet_id: int) -> PetBody:
    pet_data = PetBody(
        id=pet_id,
        category={"id": random.randrange(0, 999999), "name": fake.first_name()},
        name=fake.first_name(),
        photoUrls=[fake.image_url()],
        tags=[{"id": 1, "name": "Tag1"}],
        status=random.choice(["available", "pending", "sold"]),
    )
    api.delete_pet(pet_id)
    api.create_pet(pet_data.model_dump())

    return pet_data
