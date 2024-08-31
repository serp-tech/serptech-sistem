from django.db import models
from django.contrib.auth.models import User
from stock.models import Sector, Unit

OFFICE_STATUS = (
    ('Estagiário', 'Estagiário'),
    ('Auxiliar', 'Auxiliar'),
    ('Assistente', 'Assistente'),
    ('Gerente', 'Gerente'),
    ('Diretor', 'Diretor'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_image/', blank=True, null=True)
    sector = models.ManyToManyField(Sector, related_name='user_sector')
    unit =models.ManyToManyField(Unit, related_name='user_unit')
    position = models.CharField(max_length=50, choices=OFFICE_STATUS)


    def __str__(self):
        return self.user.first_name
    