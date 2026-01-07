from django.contrib import admin
from .models import Transaction, Payment, Debt, BuildingFund


@admin.register(BuildingFund)
class BuildingFundAdmin(admin.ModelAdmin):
    '''
    مدیریت صندوق مالی ساختمان
    '''
    list_display = ('building', 'balance', 'updated_at')
    search_fields = ('building__name',)
    readonly_fields = ('updated_at',)
    ordering = ('-updated_at',)
    autocomplete_fields = ('building',)



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    '''
    مدیریت تراکنش‌های مالی واقعی (درآمد / هزینه)
    '''
    list_display = (
        'title',
        'building',
        'transaction_type',
        'amount',
        'date',
        'created_by',
        'fund_balance_display',
    )

    list_filter = ('transaction_type', 'building', 'date')
    search_fields = (
        'title',
        'description',
        'building__name',
        'created_by__first_name',
        'created_by__last_name',
    )

    ordering = ('-date',)
    autocomplete_fields = ('building', 'created_by')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'transaction_type',
                'building',
                'created_by',
                'amount',
                'date',
            )
        }),
        ('توضیحات', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def fund_balance_display(self, obj):
        '''
        نمایش موجودی فعلی صندوق ساختمان
        '''
        fund = getattr(obj.building, 'fund', None)
        return f"{fund.balance:,} ریال" if fund else "—"

    fund_balance_display.short_description = 'موجودی صندوق'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    '''
    مدیریت پرداخت‌ها
    '''
    list_display = (
        'paid_by',
        'debt',
        'amount_paid',
        'method',
        'status',
        'paid_at',
    )

    list_filter = ('method', 'status', 'paid_at')
    search_fields = (
        'paid_by__first_name',
        'paid_by__last_name',
        'debt__title',
    )

    autocomplete_fields = ('paid_by', 'debt', 'transaction')
    readonly_fields = ('paid_at',)



@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    '''
    مدیریت بدهی‌ها (شارژ ماهانه / هزینه‌ها)
    '''
    list_display = (
        'title',
        'building',
        'unit_number',
        'responsible',
        'amount_due',
        'due_date',
        'is_paid',
    )

    list_filter = ('is_paid', 'building', 'due_date')
    search_fields = (
        'title',
        'building__name',
        'responsible__first_name',
        'responsible__last_name',
    )

    autocomplete_fields = ('building', 'responsible')
    ordering = ('due_date',)
