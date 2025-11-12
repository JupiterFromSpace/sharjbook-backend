from django.contrib import admin
from .models import Transaction, Payment, Debt


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'building',
        'transaction_type',
        'amount',
        'date',
        'is_paid',
        'created_by',
    )
    list_filter = ('transaction_type', 'is_paid', 'building', 'date')
    search_fields = ('title', 'description', 'building__name', 'created_by__first_name', 'created_by__last_name')
    ordering = ('-date',)
    autocomplete_fields = ('building', 'created_by')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'transaction_type',
                'building',
                'created_by',
                'amount',
                'date',
                'is_paid',
            )
        }),
        ('جزئیات بیشتر', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'resident',
        'transaction',
        'amount_paid',
        'method',
        'paid_at',
        'reference_code',
    )
    list_filter = ('method', 'paid_at', 'transaction__building')
    search_fields = (
        'resident__first_name',
        'resident__last_name',
        'transaction__title',
        'reference_code',
    )
    autocomplete_fields = ('resident', 'transaction')
    readonly_fields = ('paid_at',)


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = (
        'resident',
        'building',
        'title',
        'amount_due',
        'due_date',
        'is_paid',
    )
    list_filter = ('is_paid', 'building', 'due_date')
    search_fields = (
        'resident__first_name',
        'resident__last_name',
        'title',
        'building__name',
    )
    autocomplete_fields = ('resident', 'building')
    ordering = ('due_date',)
