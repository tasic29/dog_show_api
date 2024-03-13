# from model_bakery import baker
# from rest_framework import status
# import pytest

# from exibition.models import Breed


# @pytest.fixture
# def create_breed(api_client):
#     def do_create_breed(breed):
#         return api_client.post('/exibition/breeds/', breed)
#     return do_create_breed


# @pytest.mark.django_db
# class TestCreateBreed:
#     def test_if_user_is_not_admin_returns_401(self, create_breed):

#         response = create_breed({'name': 'a', 'description': 'a'})

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_invalid_data_returns_400(self, authenticate, create_breed):
#         authenticate(is_staff=True)

#         response = create_breed({'name': '', 'description': 'a'})

#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_if_valid_data_returns_201(self, authenticate, create_breed):
#         authenticate(is_staff=True)

#         response = create_breed({'name': 'a', 'description': 'a'})

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['id'] > 0


# @pytest.mark.django_db
# class TestRetrieveBreed:
#     def test_if_breed_exists_returns_200(self, api_client):
#         breed = baker.make(Breed)

#         response = api_client.get(f'/exibition/breeds/{breed.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'id': breed.id,
#             'name': breed.name,
#             'description': breed.description
#         }


# @pytest.mark.django_db
# class TestUpdateBreed:
#     def test_if_updated_breed_returns_200(self, api_client, authenticate):
#         authenticate(is_staff=True)
#         breed = baker.make(Breed)
#         updated_data = {'name': 'a', 'description': 'b'}

#         response = api_client.put(
#             f'/exibition/breeds/{breed.id}/', updated_data)

#         assert response.status_code == status.HTTP_200_OK


# @pytest.mark.django_db
# class TestDeleteBreed:
#     def test_if_deleted_breed_returns_204(self, api_client, authenticate):
#         authenticate(is_staff=True)
#         breed = baker.make(Breed)

#         response = api_client.delete(
#             f'/exibition/breeds/{breed.id}/')

#         assert response.status_code == status.HTTP_204_NO_CONTENT
