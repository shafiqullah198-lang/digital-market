from django.urls import path
from .views import login_view, signup_view
from django.contrib.auth.views import LogoutView
from .import views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('withdraw/', views.withdraw_request, name='withdraw_request'),
    


]
