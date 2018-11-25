from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Consulta(models.Model):
    valor_imovel = models.FloatField(validators=[MinValueValidator(0.0)])
    taxa_juro = models.FloatField(validators=[MinValueValidator(0.0)])
    percentual_entrada = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    quantidade_parcelas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(45.0)])
    renda_individuo = models.FloatField(validators=[MinValueValidator(1)])

    def __init__(self, data):
        super(Consulta, self).__init__()
        set_data_in_objects(self, data)

    @property
    def maximo_parcela(self):
        return self.renda_individuo * 0.3

    def capaz_pagar(self, lista_parcelas):
        capaz, pagar
        for i in range(len(lista_parcelas)):
            item = lista_parcelas[i]
            valor = item['valor']
            capaz = False
            if valor <= self.maximo_parcela:
                capaz = True
            lista_parcelas[i]['capaz_de_pagar'] = capaz
        return lista_parcelas


def set_data_in_objects(obj, data):
    for key, value in data.items():
        setattr(obj, key, value)