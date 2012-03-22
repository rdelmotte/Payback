from django.contrib import admin
from models import Expense, Payment, Group, Membership

class PaymentInline(admin.TabularInline):
    raw_id_fields       = ('user',)
    extra               = 2
    model               = Payment

class MembershipInline(admin.TabularInline):
    raw_id_fields       = ('user',)
    extra               = 2
    model               = Membership

class GroupAdmin(admin.ModelAdmin):
    date_hierarchy      = 'update'
    ordering            = ('-update',)
    search_fields       = ['name',]
    list_display        = ('name',
                           'creator',
                           'members_count',
                           'members_names',
        )
    list_filter         = ('creator', 'pubdate', 'update')
    filter_horizontal   = ('members',)
    raw_id_fields       = ('creator',)
    inlines             = (MembershipInline,)

class ExpenseAdmin(admin.ModelAdmin):
    date_hierarchy      = 'update'
    ordering            = ('-update',)
    search_fields       = ['name',]
    list_display        = ('name',
                           'pubdate',
                           'update',
                           'group',
                           'date',
                           'num_loaners',
                           'amount',
        )
    list_filter         = ('date', 'date',)
    raw_id_fields       = ('group', 'creator',)
    inlines             = (PaymentInline,)
    fieldsets           = [
        (None, {
            'classes'   : ('wide',),
            'fields'    : ('name', 'date',)
        }),
        ('Metadata', {
            'classes'   : ('wide',),
            'fields'    : ('creator', 'group')
        }),
    ]

admin.site.register(Group, GroupAdmin)
admin.site.register(Expense, ExpenseAdmin)