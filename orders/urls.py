from django.urls import re_path

from orders.views import OrderView

urlpatterns = [
    re_path(r'^orders/$', OrderView.as_view(), name="orders"),
]
