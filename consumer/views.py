from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Consulta, Individuo, Configuracoes
from .serializers import ConsultaSerializer
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import requests



class ConsultaCreateAPIView(CreateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            individuo = Individuo()
            individuo.set_data_in_object(serializer.validated_data)
            individuo.save()

            config = Configuracoes.objects.filter_by(is_active=True).first()

            serializer.validated_data['percentual_entrada'] = config.percentual_entrada
            serializer.validated_data['taxa_juro'] = config.taxa_juro

            response = requests.post(settings.URL_CONSULTA, data=request.data)
            consulta = Consulta()
            consulta.set_data_in_object(serializer.validated_data)

            consulta.individuo = individuo
            consulta.simulacao = consulta.capaz_pagar(response.json(), config)
            consulta.save()

            return Response(consulta.simulacao)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
