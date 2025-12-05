from django.urls import path
from .views import( ListBuildingFundView , ShowDemandFromResidentsView , ShowDebtorsListView,
ListIncomeTransactionsView,ListExpenseTransactionsView,)

app_name = 'finance'

urlpatterns = [
    path('show-fund/', ListBuildingFundView.as_view(), name='list-building-fund'),
    path('demand-from-residents/', ShowDemandFromResidentsView.as_view(), name='demand-from-residents'),
    path('debtors-list/', ShowDebtorsListView.as_view(), name='debtors-list'),
    path('transactions/income/', ListIncomeTransactionsView.as_view(), name='transactions-income'),
    path('transactions/expense/', ListExpenseTransactionsView.as_view(), name='transactions-expense'),

]
