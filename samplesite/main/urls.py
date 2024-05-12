from django.urls import path

from .views import index, other_page, BBloginView

app_name = 'main'
urlpatterns = [
    path('accounts/login/', BBloginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]