from django.urls import path
from .views import( ListBuildingFundView , ShowDemandFromResidentsView , ShowDebtorsListView,
ListIncomeTransactionsView,ListExpenseTransactionsView,)

app_name = 'finance'

urlpatterns = [
    path('show-fund/<uuid:building_id>/', ListBuildingFundView.as_view(), name='list-building-fund'),
    path('demand-from-residents/<uuid:building_id>/', ShowDemandFromResidentsView.as_view(), name='demand-from-residents'),
    path('debtors-list/<uuid:building_id>/', ShowDebtorsListView.as_view(), name='debtors-list'),
    path('transactions/income/<uuid:building_id>/', ListIncomeTransactionsView.as_view(), name='transactions-income'),
    path('transactions/expense/<uuid:building_id>/', ListExpenseTransactionsView.as_view(), name='transactions-expense'),

]
