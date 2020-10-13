from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self,email,dob,gender,accountType,username,password=None):
        user = self.model(email=email,dob=dob,gender=gender,accountType=accountType,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_super_user(self,email,dob,gender,accountType,username,password=None):
        user = self.model(email=email,dob=dob,gender=gender,accountType=accountType,username=username,password=password)
        user.is_admin = True
        
        user.save(using=self._db)
        return user

class User(AbstractUser):
    GENDER_CHOICES = (('M','Male'),('F','Female'),('O','Other'))
    USER_CHOICES = (('A','Artist'),('C','Consumer'),('S','SuperUser'))
    dob = models.DateField()
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    accountType = models.CharField(max_length=1,choices=USER_CHOICES)

    REQUIRED_FIELDS = ['email','dob','gender','accountType']

class Consumer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='consumer_account')


class Artist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='artist_account')