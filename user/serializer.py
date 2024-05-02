from rest_framework import serializers
from user.models import User,IdentityDocument
from rest_framework.schemas import AutoSchema
import coreapi

class IdentityDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityDocument
        fields = (
            "document_type",
            "number"
        )


class UserSerializer(serializers.ModelSerializer):
    identity_document = IdentityDocumentSerializer()

    class Meta:
        model = User
        fields = (
            "name",
            "password",
            "last_name",
            "email",
            "genre",
            "phone",
            "date_born",
            "identity_document"
        )

    def create(self, validated_data):
        identity_data = validated_data.pop('identity_document', None)
        if not identity_data: 
            raise Exception("inexistent?")

        identity = IdentityDocument.objects.create(**identity_data)
        validated_data['identity_document'] = identity
        user = User.objects.create(**validated_data)
        return user