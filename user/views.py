from rest_framework import viewsets
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
import rest_framework.status as status

from user.serializer import UserSerializer,IdentityDocumentSerializer
from user.models import User,IdentityDocument

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            return Response(
                serializer.errors,
                status=status.HTTP_409_CONFLICT
            )

        user.password = request.data['password']
        user.save()

        return Response({
            "user": serializer.data
        })

class IdentityDocumentViewSet(viewsets.ModelViewSet):
    queryset = IdentityDocument.objects.all()
    serializer_class = IdentityDocumentSerializer

    def create() -> None : None