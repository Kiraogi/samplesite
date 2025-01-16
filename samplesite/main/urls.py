from django.urls import path
from .views import rubric_bbs, bb_detail, profile_bb_detail, profile_bb_add, profile_bb_edit, profile_bb_delete
from django.conf import settings
from django.conf.urls.static import static

from .views import (index, other_page, BBloginView, profile,
                    BBLogoutView, ProfileEditView, PasswordEditView, RegisterView,
                    RegisterDoneView, user_activate, ProfileDeleteView)

app_name = 'main'
urlpatterns = [
    path('accounts/profile/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/password/edit/', PasswordEditView.as_view(), name='password_edit'),
    path('accounts/profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/profile/edit/<int:pk>/', profile_bb_edit, name='profile_bb_edit'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name='profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BBloginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', bb_detail, name='bb_detail'),
    path('<int:pk>/', rubric_bbs, name='rubric_bbs'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)