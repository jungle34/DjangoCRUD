#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Users, Tokens
from .auth import PassTokenizer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
    
    def create(self, validated_data):
        # Tokenize password
        pass_key = PassTokenizer(validated_data['password']).tokenize()
        validated_data['password'] = pass_key['pass']
        
        # Create user
        user = Users.objects.create(**validated_data)                
                
        # Save salt to validate password
        Tokens.objects.create(user=user, token=pass_key['salt'])                
        
        return user
    
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user', 'token']
        
    # Overwrite create method
    def create(self, validated_data):
        return Tokens.objects.create(validated_data)
    
    # Overwrite update method
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.token = validated_data.get('token', instance.token)
        instance.row_active = validated_data.get('row_active', instance.row_active)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance