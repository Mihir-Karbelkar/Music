from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from authentication.models import User,Artist,Consumer


class UserCreationForm(forms.ModelForm):
    
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'dob')

    def clean_confirmpassword(self):
        password = self.cleaned_data.get("password")
        confirmpassword = self.cleaned_data.get("confirmpassword")
        if password and confirmpassword and password != confirmpassword:
            raise ValidationError("passwords don't match")
        return confirmpassword

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
 
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'dob', 'is_active', )

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    
    list_display = ('email', 'dob', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('dob',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dob', 'password', 'confirmPassword'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.register(Artist)
admin.site.register(Consumer)
admin.site.unregister(Group) # Permission management not needed