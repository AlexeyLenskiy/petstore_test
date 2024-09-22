import random

import pytest
from faker import Faker

from controllers.pet_controller import PetController
from models.pet import Pet, PetBody

api = PetController()
fake = Faker(locale="ru_RU")


@pytest.mark.usefixtures("delete_pets")
@pytest.mark.parametrize(
    "pet_data",
    [
        PetBody(
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
        ),
        PetBody(
            id=0,
            name=fake.first_name(),
            photoUrls=[fake.image_url(), fake.image_url(), fake.image_url()],
        ),
        PetBody(
            id=1,
            name="И",
            photoUrls=[fake.image_url()],
        ),
        PetBody(
            id=2,
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            tags=[{"id": 1, "name": "Tag1"}],
        ),
        PetBody(
            id=3465465,
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            tags=[{"id": 1, "name": "Tag1"}, {"id": 6, "name": "Tag6"}],
        ),
        PetBody(
            id=9_223_372_036_854_775_806,
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            status="available",
        ),
        PetBody(
            id=9_223_372_036_854_775_807,
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            status="pending",
        ),
        PetBody(
            id=random.randrange(100, 1_000_000_000),
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            status="sold",
        ),
        PetBody(
            id=random.randrange(100, 1_000_000_000),
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            tags=[{"id": 1, "name": "Tag1"}],
            status="available",
        ),
    ],
)
def test_create_pet_valid_data(pet_data: PetBody):
    response = api.create_pet(pet_data.model_dump(exclude_none=True))
    assert response.status_code == 200

    pet = Pet(**response.json())
    assert pet.name == pet_data.name
    assert pet.status == pet_data.status

    # Verify that pet was created and GET pet/{petId} returns info about pet
    pet_info_response = api.get_pet(pet.id)
    assert pet_info_response.status_code == 200
    pet_info = Pet(**pet_info_response.json())
    assert pet == pet_info


@pytest.mark.usefixtures("create_pet")
@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_delete_pet(pet_id):
    response = api.delete_pet(pet_id)
    assert response.status_code == 200

    # Verify that pet no longer exists
    response = api.get_pet(pet_id)
    assert response.status_code == 404


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_get_pet_by_status(status: str):
    status_arg = f"?status={status}"
    response = api.get_pet_by_status(status_arg)
    assert response.status_code == 200

    pets = tuple(Pet(**_) for _ in response.json())
    for pet in pets:
        assert pet.status == status


@pytest.mark.usefixtures("create_pet")
@pytest.mark.parametrize(
    "values",
    [
        PetBody(
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
        ),
        PetBody(
            name=fake.first_name(),
            tags=[{"id": 10, "name": "Tag10"}],
        ),
        PetBody(
            name=fake.first_name(),
            status="available",
        ),
        PetBody(
            photoUrls=[fake.image_url()],
            tags=[{"id": 5, "name": "Tag05"}],
        ),
        PetBody(
            photoUrls=[fake.image_url()],
            status="pending",
        ),
        PetBody(
            tags=[{"id": 0, "name": "Tag0"}],
            status="sold",
        ),
        PetBody(
            id=random.randrange(100, 1_000_000_000),
            name=fake.first_name(),
            photoUrls=[fake.image_url()],
            tags=[{"id": 1, "name": "Tag1"}],
            status="available",
        ),
    ],
)
@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_update_pet(values: PetBody, create_pet: PetBody, pet_id: int):
    update_body = values.model_dump(exclude_none=True)
    update_body.update({"id": pet_id})

    response = api.update_pet(update_body)
    assert response.status_code == 200

    # Verify that pet info was updated
    pet = api.get_pet(pet_id)
    assert response.json() == pet.json()
