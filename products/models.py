from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class Product(models.Model):
    #id = models.AutoField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=220, help_text='Enter field documentation')
    content = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)

