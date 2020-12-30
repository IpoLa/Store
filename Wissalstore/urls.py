from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from accounts.views import (
    login_view,
    logout_view,
    register_view,
)
from products.views import (
    home__view,
    product__create__view,
    product__detail__view,
    product__api__detail__view,
    product__list__view,
    featured_product_view,
    product__delete__view,
    product__action__view
)
from orders.views import (
    order_checkout_view,
    download_order,
    my_orders_view
)

from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('', home__view),
    # path('', TemplateView.as_view(template_name='base.html')),
    path('checkout/', order_checkout_view),
    path('success/', my_orders_view),
    path('orders/', my_orders_view),
    path('featured/', featured_product_view),
    path('products/', product__list__view),
    path('products/create/', product__create__view),
    path('products/<int:id>/', product__detail__view),
    path('orders/<int:order_id>/download/', download_order),
    path('api/products/action/', product__action__view),
    path('api/products/<int:id>/delete', product__delete__view),
    # path('api/products/<int:id>/', product__api__detail__view),
    re_path(r'api/products/(?P<pk>\d+)/', product__api__detail__view),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)