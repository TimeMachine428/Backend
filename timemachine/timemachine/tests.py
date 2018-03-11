from rest_framework.test import APITestCase
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class JWTAPITestCase(APITestCase):
    authenticated_user = None

    def authenticate(self, user):
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)
