from rest_framework import serializers
from .models import Consulta, Individuo
from django.core.validators import MaxValueValidator, MinValueValidator

class IndividuoSerializer(serializers.ModelSerializer)


class ConsultaSerializer(serializers.ModelSerializer):
    cpf = serializers.CharField(max_length=14)
    nome_completo = serializers.CharField(max_length=256)
    data_nascimento = serializers.DateField()
    tem_fgts = serializers.BooleanField()
    email = serializers.EmailField(allow_blank=True)
    valor_fgts = serializers.FloatField(min_value=0, default=0)

    class Meta:
        model = Consulta
        exclude = ('individuo', 'simulacao')


class ConsultaEmailSerializer(serializers.ModelSerializer):
    individuo = IndividuoSerializer()

    class Meta:
        model = Consulta
        fields = '__all__'

