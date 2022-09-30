from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile, ContactMail, Inbox
# Register your models here.


class UserAdministrator(UserAdmin):
    list_display= ('id', 'email', 'username', 'date_joined', 'is_active', 'is_admin', 'is_deactivated','last_login' )
    search_fields=('email', 'username')
    readonly_fields=('date_joined', 'last_login', 'is_active', 'id')
    
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    
admin.site.register(User, UserAdministrator)


admin.site.register(Profile)
admin.site.register(ContactMail)
admin.site.register(Inbox)

