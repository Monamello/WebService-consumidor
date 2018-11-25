from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import Consulta
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

            serializer.validated_data['percentual_entrada'] = 20
            serializer.validated_data['taxa_juro'] = 10

            response = requests.post(settings.URL_CONSULTA, data=request.data)
            consulta = Consulta(serializer.validated_data)
            return Response(consulta.capaz_pagar(response.json()))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
