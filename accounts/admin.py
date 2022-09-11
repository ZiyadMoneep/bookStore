from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Author

# Register your models here.

Author = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Author
    list_display = ['email', 'username', 'age', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )


admin.site.register(Author, CustomUserAdmin)
