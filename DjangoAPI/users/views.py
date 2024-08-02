from django.shortcuts import render  
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

from .models import Users, Tokens
from .serializers import UserSerializer, TokenSerializer

from .auth import PassTokenizer

class TokenView(APIView):
    def get(self, request):
        result = Tokens.objects.all()
        serializers = TokenSerializer(result)
        
        return serializers.data
  
class UserView(APIView): 
        
    def get(self, request, id=None):
        if id:
            get_object_or_404(Users, id=id)
            
            result = Users.objects.get(id=id)
            serializers = UserSerializer(result)
            
            tokens = Tokens.objects.get(user=result)
            token_serializer = TokenSerializer(tokens)

            return Response({'success': 'success', 'users': serializers.data, 'token': token_serializer.data}, status=200)

        result = Users.objects.all()  
        serializers = UserSerializer(result, many=True)  
        return Response({'status': 'success', "students": serializers.data}, status=200)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  
        else:
            return Response({'status': 'error', 'msg': 'invalid data to post'}, status=400)
        
    def delete(self, request, id=None):
        result = get_object_or_404(Users, id=id)  
        result.delete()  
        return Response({"status": "success", "data": "Record Deleted"})
