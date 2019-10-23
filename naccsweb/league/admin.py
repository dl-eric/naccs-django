from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Team, School, Player, Payment, Division


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_paid')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'division', 'is_active', 'is_ready')


class TeamInline(admin.StackedInline):
    model = Team
    can_delete = False
    verbose_name_plural = 'Teams'
    fk_name = 'school'


class SchoolAdmin(admin.ModelAdmin):
    inlines = (TeamInline, )
    list_display = ('name', 'city', 'state', 'is_active')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(SchoolAdmin, self).get_inline_instances(request, obj)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paymentid', 'payerid', 'date')


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Division)