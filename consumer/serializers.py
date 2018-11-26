from rest_framework import serializers
from .models import Consulta, Individuo
from django.core.validators import MaxValueValidator, MinValueValidator


class ConsultaSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)
    nome_completo = serializers.CharField(max_length=256)
    data_nascimento = serializers.DateField()
    tem_fgts = serializers.BooleanField()
    valor_fgts = serializers.FloatField(validators=[MinValueValidator(0)])
    max_parcela_individuo = serializers.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    taxa_juro = serializers.FloatField(validators=[MinValueValidator(0.0)])
    percentual_entrada = serializers.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    class Meta:
        model = Consulta
        exclude = ('individuo', )

