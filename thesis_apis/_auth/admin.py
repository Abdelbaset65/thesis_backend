from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, RadiologistProfile
from django import forms


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'activated')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone', 'activated')
    readonly_fields = ('last_login', 'date_joined', 'password')
    list_filter = ('is_admin', 'activated')
    fieldsets = (
        ('Basic info', {
            'fields': ('email', 'password', 'last_login', 'date_joined')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('activated', 'is_admin',
                                    'is_active', 'is_staff', 'is_superuser')}),
        ('Group Permissions', {
            'fields': ('groups', 'user_permissions',)
        }),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a _auth.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('-date_joined',)
    filter_horizontal = ()


class RadiologistProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'updated_at')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RadiologistProfile, RadiologistProfileAdmin)
