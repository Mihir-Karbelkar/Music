from django.contrib.auth import get_user_model
from rest_framework import serializers
from authentication.models import Artist,Consumer

User = get_user_model()

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    dob = serializers.DateField()
    password = serializers.CharField(write_only=True,required=True)
    confirmPassword = serializers.CharField(write_only=True,required=True)
    gender = ChoiceField(choices=User.GENDER_CHOICES)
    accountType = ChoiceField(choices=User.USER_CHOICES)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirmPassword",
            "dob",
            "gender",
            "accountType"
        ]
        extra_lwargs = {"password":{"wrote_only":True}}
    
    def create(self,validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        confirmPassword = validated_data["confirmPassword"]
        dob = validated_data["dob"]
        gender = validated_data["gender"]
        accountType = validated_data["accountType"]
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
            {"email":"Email address already exists"}
        )

        if password != confirmPassword:
            raise serializers.ValidationError(
            {"password":"The two passwords differ."}
        )

        user = User(username=username,email=email,dob= dob,gender= gender,accountType=accountType)

        user.set_password(password)

        user.save()
        if user.accountType == 'A':
            artist = Artist.objects.create(user=user)
        else:
            consumer = Consumer.objects.create(user=user)

        return user

class ArtistSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)