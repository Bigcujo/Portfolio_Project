from django.urls import path
from .views import register, profile
from .views import ( 
    CustomLoginView, 
    CustomLogoutView, 
    UserPostListView, 
    UserPasswordResetView, 
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView
) 
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Add your URL patterns here
   path('register/', register, name='user-register'),
   path('login/', CustomLoginView.as_view(), name='user-login'),
   path('logout/', CustomLogoutView.as_view(), name='user-logout'),
   path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
   path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
   path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
   path('profile/', profile, name='user-profile'),
   path('<str:username>/', UserPostListView.as_view(), name='user-posts'),
   

   
   


  
    # Add other paths as needed
]
