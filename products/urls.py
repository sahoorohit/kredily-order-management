from django.urls import re_path

from products.views import ProductView

urlpatterns = [
    re_path(r'^products/$', ProductView.as_view(), name="products"),
]
