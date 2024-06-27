from rest_framework import serializers
from rest_framework.utils.serializer_helpers import json
from user.models import AuthUser, UserDetails

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            "password",
            "email",
        )

class UserDetailsSerializer(serializers.ModelSerializer):
    def to_string(self):
        return json.dumps(self.data)

    class Meta:
        model = UserDetails
        fields = (
            "first_name",
            "last_name",
            "genre",
            "phone",
            "date_born",
            "document_type",
            "document_number",
        )

