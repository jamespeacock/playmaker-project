from django.contrib import admin

from playmaker.login.forms import CustomUserChangeForm, CustomUserCreationForm
from playmaker.models import User, Device


# Register your models here.
from playmaker.shared.models import SPModel


class SPModelAdmin(admin.ModelAdmin):
    pass


class DeviceAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'sp_username', 'name', 'sp_id']


admin.site.register(SPModel, SPModelAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Device, DeviceAdmin)
