import random

import pytest
from faker import Faker

from controllers.pet_controller import PetController
from helpers.helpers import get_request_info
from models.pet import ErrorBody, Pet, PetBody

api = PetController()
fake = Faker(locale="ru_RU")


@pytest.mark.usefixtures("delete_pets")
@pytest.mark.parametrize(
    "pet_data",
    [
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="required only (name, photoUrls)",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[],
            ),
            id="empty list in photoUrls",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url(), fake.image_url(), fake.image_url()],
            ),
            id="multiple photoUrls",
        ),
        pytest.param(
            PetBody(
                name="И",
                photoUrls=[fake.image_url()],
            ),
            id="name with 1 symbol",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                tags=[{"id": 1, "name": "Tag1"}],
            ),
            id="with tags",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                tags=[],
            ),
            id="empty list in tags",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                tags=[{"id": 1, "name": "Tag1"}, {"id": 6, "name": "Tag6"}],
            ),
            id="multiple tags",
        ),
        pytest.param(
            PetBody(
                id=0,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id=0",
        ),
        pytest.param(
            PetBody(
                id=1,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id=1",
        ),
        pytest.param(
            PetBody(
                id=9_223_372_036_854_775_806,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id = max int64 - 1 value",
        ),
        pytest.param(
            PetBody(
                id=9_223_372_036_854_775_807,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id = max int64 value",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                status="available",
            ),
            id="status=available",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                status="pending",
            ),
            id="status=pending",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                status="sold",
            ),
            id="status=sold",
        ),
        pytest.param(
            PetBody(
                id=random.randrange(100, 1_000_000_000),
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                tags=[{"id": 1, "name": "Tag1"}],
                status="available",
            ),
            id="with all fields",
        ),
    ],
)
def test_create_pet_valid_data(pet_data: PetBody):
    """
    Test is checking that method POST /pet with inputed valid data creates new pet in DB
    """
    response = api.create_pet(pet_data.model_dump(exclude_none=True))
    assert response.status_code == 200, get_request_info(response)

    pet = Pet(**response.json())
    assert pet.name == pet_data.name
    assert pet.status == pet_data.status

    # Verify that pet was created and GET pet/{petId} returns info about pet
    pet_info_response = api.get_pet(pet.id)
    assert pet_info_response.status_code == 200, get_request_info(pet_info_response)
    pet_info = Pet(**pet_info_response.json())
    assert pet == pet_info


@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_create_pet_with_existed_id(create_pet):
    """
    Test is checking that method POST /pet cannot create new pet wit existed id
    """
    pet_data = create_pet
    response = api.create_pet(pet_data.model_dump(exclude_none=True))
    assert response.status_code == 405, get_request_info(response)


@pytest.mark.parametrize(
    "pet_data",
    [
        pytest.param(PetBody(), id="empty body"),
        pytest.param(
            PetBody(
                photoUrls=[fake.image_url()],
            ),
            id="without required field 'name'",
        ),
        pytest.param(
            PetBody(
                name=fake.first_name(),
            ),
            id="without required field 'photoUrls'",
        ),
        pytest.param(
            PetBody(
                id=-1,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id < 0",
        ),
        pytest.param(
            PetBody(
                id=None,
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id=Null",
        ),
        pytest.param(
            PetBody(
                id="519b34fc-dba9-442a-928c-f5b6626367a8",
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
            ),
            id="id not int (uuid4)",
        ),
        pytest.param(
            PetBody(
                id=random.randrange(100, 1_000_000_000),
                name=fake.first_name(),
                photoUrls=[11, 1567],
            ),
            id="photoUrls not in str",
        ),
        pytest.param(
            PetBody(
                id=random.randrange(100, 1_000_000_000),
                photoUrls=[fake.image_url()],
                tags=[None],
            ),
            id="tags = Null",
        ),
        pytest.param(
            PetBody(
                id=random.randrange(100, 1_000_000_000),
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                tags=[{"id": 1, "name": 1}],
            ),
            id="tags->name not in string format",
        ),
        pytest.param(
            PetBody(
                id=random.randrange(100, 1_000_000_000),
                name=fake.first_name(),
                photoUrls=[fake.image_url()],
                status="not_existed_status",
            ),
            id="not supported status",
        ),
    ],
)
def test_create_pet_invalid_data(pet_data: PetBody):
    """
    Test is checking that method POST /pet with invalid inputs returns error
    """
    response = api.create_pet(pet_data.model_dump(exclude_none=False))
    assert response.status_code == 405, get_request_info(response)


@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_get_pet_with_valid_id(create_pet, pet_id: int):
    """
    Test is checking that method GET  /pet/{petId} get info about pet
    """
    pet = create_pet
    response = api.get_pet(pet_id)
    assert response.status_code == 200, get_request_info(response)

    pet_info = Pet(**response.json())
    assert pet == pet_info


@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_get_pet_with_not_existed_id(pet_id: int):
    """
    Test is checking that method GET  /pet/{petId} returns valid error for not existed id
    """
    api.delete_pet(pet_id)
    response = api.get_pet(pet_id)
    assert response.status_code == 404, get_request_info(response)

    error = ErrorBody(code=1, type="error", message="Pet not found")
    assert response.json() == error.model_dump()


@pytest.mark.usefixtures("create_pet")
@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_delete_pet(pet_id):
    """
    Test is checking that method DELETE /pet/{petId} deletes pet by id
    """
    response = api.delete_pet(pet_id)
    assert response.status_code == 200

    # Verify that pet no longer exists
    response = api.get_pet(pet_id)
    assert response.status_code == 404


@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_delete_pet_with_not_existed_id(pet_id: int):
    """
    Test is checking that method DELETE /pet/{petId} returns valid error for not existed id
    """
    api.delete_pet(pet_id)
    response = api.delete_pet(pet_id)
    assert response.status_code == 404, get_request_info(response)


@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_get_pet_by_status(status: str):
    """
    Test is checking that method GET  /pet/findByStatus get info about all pets with required status
    """
    status_arg = f"?status={status}"
    response = api.get_pet_by_status(status_arg)
    assert response.status_code == 200, get_request_info(response)

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
def test_update_pet(values: PetBody, pet_id: int):
    """
    Test is checking that method PUT /pet updates pet info
    """
    update_body = values.model_dump(exclude_none=True)
    update_body.update({"id": pet_id})

    response = api.update_pet(update_body)
    assert response.status_code == 200

    # Verify that pet info was updated
    pet = api.get_pet(pet_id)
    assert response.json() == pet.json()


@pytest.mark.parametrize("pet_id", [random.randrange(100, 1_000_000_000)])
def test_update_pet_with_not_existed_id(pet_id: int):
    """
    Test is checking that method PUT /pet/{petId} returns valid error for not existed id
    """
    pet = PetBody(
        id=pet_id,
        name=fake.first_name(),
        photoUrls=[fake.image_url()],
        tags=[{"id": 1, "name": "Tag1"}],
        status="available",
    )
    api.delete_pet(pet_id)
    response = api.update_pet(pet.model_dump())
    assert response.status_code == 404, get_request_info(response)
