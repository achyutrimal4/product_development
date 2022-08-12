from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.


class UserAdministrator(UserAdmin):
    list_display= ('email', 'username', 'date_joined', 'country', 'full_name','is_active','last_login', 'is_admin', 'is_staff' )
    search_fields=('email', 'username', 'full_name', 'country')
    readonly_fields=('date_joined', 'last_login', 'is_active')
    
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    
admin.site.register(User, UserAdministrator)