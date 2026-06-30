from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model

# with out authentication!!!

class TestGetBuilding:
    def test_get_unauthorized_response_401_status(self):
        client = APIClient()
        url = reverse("buildings:api-v1:my-buildings")
        response = client.get(url)
        assert response.status_code == 401
        
#==================================================        




User = get_user_model()


@pytest.mark.django_db
def test_get_buildings_authenticated_user_returns_200():
    user = User.objects.create_user(
        email="test@example.com"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("buildings:api-v1:my-buildings")
    response = client.get(url)

    assert response.status_code == 200

#==================================================