from django.urls import path
from .views import RegisterView, LoginView, Userlist


urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("userlist", Userlist.as_view(),name="userlist")
]
