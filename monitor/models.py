from django.db import models

# Create your models here.

class Clp(models.Model):
    idclp  = models.AutoField(primary_key=True)
    nome   = models.CharField(max_length=45)
    ip     = models.GenericIPAddressField(protocol='both')
    porta  = models.CharField(max_length=45)
    ativo  = models.BooleanField()

    class Meta:
        db_table = 'clp'

    def __str__(self):
        return f'{self.nome} ({self.ip}:{self.porta})'