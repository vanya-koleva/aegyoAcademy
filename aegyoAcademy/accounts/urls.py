from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from accounts import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', include([
        path('', views.ViewProfile.as_view(), name='view-profile'),
        path('edit/', views.EditProfile.as_view(), name='edit-profile'),
    ])),
]