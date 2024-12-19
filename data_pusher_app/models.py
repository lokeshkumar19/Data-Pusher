from django.db import models
import uuid
# Create your models here.
class Account(models.Model):
    email = models.EmailField(unique=True)
    account_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account_name = models.CharField(max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True)  # Generate automatically
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.account_name

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT')])

    def __str__(self):
        return f"{self.account.account_name} - {self.url}"