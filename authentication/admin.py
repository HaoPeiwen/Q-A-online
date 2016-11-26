from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import MyUser


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class MyUserAdmin(UserAdmin):
    inlines = (MyUserInline,)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
