from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    address = models.CharField(max_length=100, null=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    banner_url = models.TextField(verbose_name="URL do Banner",blank=True, null=True)
    about = models.TextField(null=True) 
    expired = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Rolês"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    def __str__(self):
        return f'{self.name}'


class Ticket(models.Model):
    type = models.CharField(unique=True, max_length=25)
    price = models.FloatField()
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)
    owner = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True)
    
    def __str__(self):
        return self.role.name+" - "+self.type
    