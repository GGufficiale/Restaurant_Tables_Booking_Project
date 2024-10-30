from django.urls import path
from django.views.decorators.cache import cache_page

from restaurant.views import BookingListView, BookingDetailView, BookingCreateView, BookingUpdateView, \
    BookingDeleteView, ContactPageView, ComplainPageView, InfoPageView, HomeView
from restaurant.apps import RestaurantConfig

app_name = RestaurantConfig.name
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    # метод для отображения отдельной страницы с товаром (по одному товару)
    path('restaurant/contact/', ContactPageView.as_view(), name='contact'),
    path('restaurant/complain/', ComplainPageView.as_view(), name='complain'),
    path('restaurant/info/', InfoPageView.as_view(), name='info'),
    # В декоратор кеширования cache_page передается время его жизни (60 сек) и ссылка на контроллер (contact).
    # Это позволяет кешировать весь контроллер
    path('restaurant/<int:pk>/', cache_page(60)(BookingDetailView.as_view()), name='booking_detail'),
    path('restaurant/list/', BookingListView.as_view(), name='booking_list'),
    path('restaurant/create/', BookingCreateView.as_view(), name='booking_create'),
    path('restaurant/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('restaurant/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_confirm_delete'),
    # path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
]
