from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Account, Plant, PlantedTree


# Inline para associar contas ao usuário no admin
class AccountInline(admin.TabularInline):
    model = User.accounts.through
    extra = 1


class UserAdmin(BaseUserAdmin):
    inlines = [AccountInline]
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_at')
    search_fields = ('user__username',)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)


class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    readonly_fields = ('user', 'latitude', 'longitude', 'planted_at')


class PlantAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [PlantedTreeInline]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(PlantedTree)
