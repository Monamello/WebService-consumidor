from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Consulta, Individuo, Configuracoes
from .serializers import ConsultaSerializer
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
import requests



class ConsultaCreateAPIView(CreateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

    def save_consulta(self, validated_data, json, config):
        individuo = Individuo()
        individuo.set_data_in_object(validated_data)
        individuo.save()
        
        consulta = Consulta()
        consulta.set_data_in_object(validated_data)

        consulta.individuo = individuo
        consulta.simulacao = consulta.capaz_pagar(json, config)
        consulta.save()
        return consulta
    
    def send_email(self, consulta):
        send_mail(
            'Consulta Financiamento',
            'Here is the message.',
            settings.EMAIL_HOST_USER,
            [consulta.individuo.email],
        )
        

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            config = Configuracoes.objects.filter(is_active=True).first()

            serializer.validated_data['percentual_entrada'] = config.percentual_entrada
            serializer.validated_data['taxa_juro'] = config.taxa_juro

            response = requests.post(settings.URL_CONSULTA, data=serializer.validated_data)
            if response.status_code == 200:

                consulta = self.save_consulta(serializer.validated_data, response.json(), config)
                if consulta.individuo.email:
                    self.send_email(consulta)

                return Response(consulta.simulacao)
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
