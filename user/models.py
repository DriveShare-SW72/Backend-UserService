from django.db import models

# Create your models here.

class IdentityDocument(models.Model):
    document_type = models.CharField(max_length=5)
    number = models.CharField(max_length=5) 
    

class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    genre = models.CharField(max_length=1)
    phone = models.CharField(max_length=50)
    date_born = models.DateField()
    identity_document = models.OneToOneField(
        IdentityDocument,
        on_delete=models.CASCADE,
        db_column='id_identity_docum',
    )

    def save(self, *args, **kwargs):
        if self.identity_document and not self.identity_document.pk:
            self.identity_document.save()
        super().save(*args, **kwargs)
