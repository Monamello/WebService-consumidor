from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator


class Configuracoes(models.Model):
    max_parcela_individuo = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    taxa_juro = models.FloatField(validators=[MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True)
    percentual_entrada = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    def set_data_in_object(self, data):
        set_data_in_objects(self, data)

    def __str__(self):
        return '%r - %r - %r - %r' % (
            self.is_active, self.taxa_juro,
            self.max_parcela_individuo, self.percentual_entrada
        )


class Consulta(models.Model):
    valor_imovel = models.FloatField(validators=[MinValueValidator(0.0)])
    quantidade_parcelas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(540.0)])
    renda_individuo = models.FloatField(validators=[MinValueValidator(1)])
    individuo = models.ForeignKey('Individuo', on_delete=models.CASCADE, null=True)
    simulacao = JSONField()

    def set_data_in_object(self, data):
        set_data_in_objects(self, data)

    def capaz_pagar(self, lista_parcelas, config):
        for i in range(len(lista_parcelas)):
            item = lista_parcelas[i]
            valor = item['valor']
            capaz = False
            if valor <= config.max_parcela_individuo:
                capaz = True
            lista_parcelas[i]['capaz_de_pagar'] = capaz
        return lista_parcelas


class Individuo(models.Model):
    cpf = models.CharField(max_length=14)
    nome_completo = models.CharField(max_length=256)
    data_nascimento = models.DateField()
    tem_fgts = models.BooleanField()
    email = models.EmailField(blank=True, null= True)
    valor_fgts = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return '{} - {}'.format(self.cpf, self.nome_completo)

    def set_data_in_object(self, data):
        set_data_in_objects(self, data)


def set_data_in_objects(obj, data):
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)