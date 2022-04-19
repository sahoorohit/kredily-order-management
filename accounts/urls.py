from django.urls import re_path

from accounts.views import LoginView, SignUpView

urlpatterns = [
    re_path(r'^signup/$', SignUpView.as_view(), name="signup"),
    re_path(r'^login/$', LoginView.as_view(), name="login"),
]
