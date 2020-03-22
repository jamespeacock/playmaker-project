from django.contrib import admin

from playmaker.login.forms import CustomUserChangeForm, CustomUserCreationForm
from playmaker.models import User, Device


# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'sp_username', 'name', 'sp_id']


admin.site.register(User, UserAdmin)
admin.site.register(Device, DeviceAdmin)
