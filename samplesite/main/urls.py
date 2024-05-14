from django.urls import path

from .views import index, other_page, BBloginView, profile, BBLogoutView

app_name = 'main'
urlpatterns = [
    path('account/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BBloginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]