from django.contrib import admin
from django.urls import path, re_path
from products.views import (
    home__view,
    product__create__view,
    product__detail__view,
    product__api__detail__view,
    product__list__view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home__view),
    path('products/', product__list__view),
    path('products/create/', product__create__view),
    path('products/<int:pk>/', product__detail__view),
    # path('api/products/<int:id>/', product__api__detail__view),
    re_path(r'api/products/(?P<pk>\d+)/', product__api__detail__view),
]
