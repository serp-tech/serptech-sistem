from django.db import models
from django.contrib.auth.models import User, Group
from stock.models import Sector, Unit

OFFICE_STATUS = (
    ('Estagiário', 'Estagiário'),
    ('Auxiliar', 'Auxiliar'),
    ('Assistente', 'Assistente'),
    ('Contador', 'Contador'),
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
    

    def save(self, *args, **kwargs):
        # Primeiro, salva o UserProfile
        super(UserProfile, self).save(*args, **kwargs)
        
        # Depois, atribui o grupo correto ao usuário
        self.assign_group()

    def assign_group(self):
        # Remove todos os grupos existentes do usuário
        self.user.groups.clear()
        
        # Verifica a posição do usuário e adiciona ao grupo correspondente
        if self.position == 'Gerente' or self.position == 'Diretor':
            group, created = Group.objects.get_or_create(name='manager')
        elif self.position == 'Assistente':
            group, created = Group.objects.get_or_create(name='assistant')
        elif self.position == 'Contador':
            group, created = Group.objects.get_or_create(name='counter')
        else:
            group, created = Group.objects.get_or_create(name='group2')
        
        # Adiciona o usuário ao grupo correspondente
        self.user.groups.add(group)