from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class AuthUserManager(BaseUserManager):
    """
    Manager for AuthUser model
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def find_by_email(self, email):
        return super().get_queryset().filter(email=email).first()

    def find_by_id(self, id):
        return super().get_queryset().filter(id=id).first()

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class AuthUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        db_table = "auth_users"

    username = None
    first_name = models.CharField(max_length=40)
    email = models.CharField(unique=True, blank=False, max_length=60)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return self.email


class UserDetailsManager(models.Manager):
    def find_by_user(self, user):
        return super().get_queryset().filter(user=user).first()

    def create_details(
        self,
        user,
        first_name,
        last_name,
        genre,
        phone,
        date_born,
        document_type,
        document_number,
    ):
        return super().create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            genre=genre,
            phone=phone,
            date_born=date_born,
            document_type=document_type,
            document_number=document_number,
        )


class UserDetails(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    genre = models.CharField(max_length=1)
    phone = models.CharField(max_length=50)
    date_born = models.DateField()
    document_type = models.CharField(max_length=5)
    document_number = models.CharField(max_length=5)

    objects = UserDetailsManager()

    class Meta:
        db_table = "user_details"
