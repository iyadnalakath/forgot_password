from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('id','username','email',"is_admin","is_active","is_superuser","is_staff","role")
   

    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()
    ordering = ('id',)


admin.site.register(Account, AccountAdmin)
