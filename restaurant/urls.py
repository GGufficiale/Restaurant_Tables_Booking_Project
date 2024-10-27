from django.urls import path
from django.views.decorators.cache import cache_page

from restaurant.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    toggle_activity, ContactPageView
from restaurant.apps import MainConfig

app_name = MainConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    # метод для отображения отдельной страницы с товаром (по одному товару)
    path('restaurant/contact/', ContactPageView.as_view(), name='contact'),
    # В декоратор кеширования cache_page передается время его жизни (60 сек) и ссылка на контроллер (contact).
    # Это позволяет кешировать весь контроллер
    path('restaurant/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='products_detail'),
    path('restaurant/create', ProductCreateView.as_view(), name='products_create'),
    path('restaurant/<int:pk>/update/', ProductUpdateView.as_view(), name='products_update'),
    path('restaurant/<int:pk>/delete/', ProductDeleteView.as_view(), name='products_delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
