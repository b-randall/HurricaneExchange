from django.contrib import admin
from .models import UserFund, FirstTime
from trading.models import Trading_Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class InlineUserFund(admin.TabularInline):
    model = UserFund

class InlineTrading(admin.TabularInline):
    model = Trading_Account
    show_change_link = True


class CustomUserAdmin(UserAdmin):
    def user_funds (self, instance):
        return instance.userfund.fund
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'user_funds')
    inlines = [InlineUserFund, InlineTrading]


class UserFundAdmin(admin.ModelAdmin):
    list_display = ('user', 'fund')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserFund, UserFundAdmin)
admin.site.register(FirstTime)
