from django.urls import path

from debts import views

app_name = 'debts'

urlpatterns = [
    path('lend/', views.lend_view, name='lend'),
]
