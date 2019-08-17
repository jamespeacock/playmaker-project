from django.contrib import admin

from playmaker.login.forms import CustomUserChangeForm, CustomUserCreationForm
from playmaker.models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'name']


admin.site.register(User, UserAdmin)
