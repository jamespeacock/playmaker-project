from django.contrib import admin

from playmaker.controller.models import Controller, Listener, Group, Device, Permission, Queue


class ControllerAdmin(admin.ModelAdmin):
    pass


class ListenerAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


class DeviceAdmin(admin.ModelAdmin):
    pass


class PermissionAdmin(admin.ModelAdmin):
    pass


class QueueAdmin(admin.ModelAdmin):
    pass


admin.site.register(Controller, ControllerAdmin)
admin.site.register(Listener, ListenerAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Queue, QueueAdmin)