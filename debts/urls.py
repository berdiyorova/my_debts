from django.urls import path

from debts import views

app_name = 'debts'

urlpatterns = [
    path('lend/', views.lend_view, name='lend'),
    path('borrow/', views.borrow_view, name='borrow'),
    path('lent/', views.my_lent_debts, name='lent'),
    path('borrowed/', views.my_borrowed_debts, name='borrowed'),
    path('<int:pk>/', views.debt_detail, name='detail'),
]
