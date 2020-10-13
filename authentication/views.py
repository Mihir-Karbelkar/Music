from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializers import UserSerializer
from django.contrib.auth import get_user_model

# Creates an account for Artist/Consumer
class UserCreate(APIView):

    def post(self,request,format='json'):
        userSerializer = UserSerializer(data=request.data)

        if userSerializer.is_valid():
            user = userSerializer.save()
            if user:
                return Response(userSerializer.data,status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
