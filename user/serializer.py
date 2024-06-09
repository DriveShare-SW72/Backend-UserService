from rest_framework import serializers
from user.models import AuthUser, UserDetails

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            "password",
            "email",
        )

class UserDetailsSerializer(serializers.ModelSerializer):
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
