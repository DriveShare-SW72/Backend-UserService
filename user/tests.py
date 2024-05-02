from django.test import TestCase
from rest_framework.test import APIRequestFactory
import requests

from user.models import User
from user.serializer import UserSerializer

# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self) -> None:
        # Base de nuestra request
        self.userbody = {
            "name": "renzo",
            "password": "rloli",
            "last_name": "loli",
            "email": "rloli@hotmail.com",
            "genre": "m",
            "phone": "999999999",
            "date_born": "2024-05-20",
            "identity_document": {
                "document_type": "DNI",
                "number": "77777"
            }
        }

        self.serializer_mock = UserSerializer(data=self.userbody)
        self.assertTrue(self.serializer_mock.is_valid())

        # Guardamos el serializado
        self.serial_user = self.serializer_mock.save()

    def test_user_login(self):

        # Serializamos y validamos
        serializer = UserSerializer(data=self.userbody)
        self.assertTrue(serializer.is_valid())

        # Guardamos el serializado
        logged_user = serializer.save()

        # Buscamos en la base local del modelo
        user = User.objects.get(id=logged_user.id)

        # Validamos si se guardo
        self.assertEqual(user, logged_user)

    def test_user_login(self):
        # Buscamos el usuario en la base
        user = User.objects.get(id=self.serial_user.id)

        # Validamos que sea igual al guardado
        self.assertEqual(user, self.serial_user)