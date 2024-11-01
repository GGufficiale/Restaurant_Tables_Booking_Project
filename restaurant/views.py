import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pytils.translit import slugify

from config.settings import EMAIL_HOST_USER
from restaurant.forms import BookingForm, BookingModeratorForm
from restaurant.models import Table, Booking
from restaurant.services import get_bookings_from_cache


# def booking_list(request):
#     """Функция принимает параметр request (инфа от пользователя на фротэнде) и возвращает ответ"""
#     bookings = Booking.objects.all()
#     context = {"bookings": bookings}
#     return render(request, 'booking_list.html', context)

class HomeView(TemplateView):
    """Класс, отображающий базовую страницу"""
    template_name = 'restaurant/index.html'


class BookingListView(LoginRequiredMixin, ListView):
    """Класс, заменяющий функцию booking_list (FBV на CBV)"""
    model = Booking
    template_name = 'restaurant/booking_list.html'

    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user)


class BookingDetailView(DetailView):
    """Класс, заменяющий функцию bookings_detail (FBV на CBV)"""
    model = Booking


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'restaurant/booking_create.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('restaurant:booking_list')
        else:
            return reverse('restaurant:index')

    # def form_valid(self, form):
    #     booking = form.save()
    #     booking.user = self.request.user
    #     times_used = booking.time.all()
    #     booked_table = Table.objects.get(pk=self.kwargs.get('pk'))
    #     times_table = booked_table.time.all()
    #     booked_table.time.set(times_table.difference(times_used))
    #     booked_table.save()
    #     booking.table = booked_table
    #     booking.save()
    #     return super().form_valid(form)

    def form_valid(self, form):
        """Метод для отправки пользователю ссылки на почту при верификации почты"""
        booking = form.save()
        user = self.request.user
        booking.owner = user
        booking.save()
        host = self.request.get_host()
        token = secrets.token_hex(16)
        user.token = token
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(subject='Подтверждение почты', message=f'Перейдите по ссылке для подтверждения почты {url}',
                  from_email=EMAIL_HOST_USER, recipient_list=[user.email])
        return super().form_valid(form)

    # def form_valid(self, form):
    # """Метод для отображения латиницей кириллических названий товара"""
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.name)
    #         new_mat.save()
    #     return super().form_valid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'restaurant/booking_create.html'
    success_url = reverse_lazy('restaurant:booking_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.name)
    #         new_mat.save()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant:booking_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        """Метод для работы с правами доступа"""
        user = self.request.user
        if user == self.object.owner:
            return BookingForm
        if user.has_perm('booking.can_cancel_publication') and user.has_perm(
                'product.can_edit_description') and user.has_perm('product.can_change_category'):
            return BookingModeratorForm
        raise PermissionDenied


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'restaurant/booking_confirm_delete.html'
    success_url = reverse_lazy('restaurant:booking_list')

    # def get_object(self, queryset=None):
    #     """Метод для определения доступа к удалению только своих бронирований"""
    #     self.object = super().get_object(queryset)
    #     if self.request.user == self.object.owner:
    #         self.object.save()
    #         return self.object
    #     raise PermissionDenied


class ContactPageView(TemplateView):
    """Класс для отображения страницы с контактами"""
    template_name = 'restaurant/contact.html'

    def post(self, request, *args, **kwargs):
        """Метод для приема инфы с фронтэнда в контактах и ее вывода в консоль"""
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(f'{name} ({email}): {message}')
        return render(request, 'restaurant/contact.html')

    def get(self, request):
        return render(request, 'restaurant/contact.html')


class ComplainPageView(TemplateView):
    """Класс для отображения страницы с жалобами"""
    template_name = 'restaurant/complain.html'

    def post(self, request, *args, **kwargs):
        """Метод для приема инфы с фронтэнда в жалобах и ее вывода в консоль"""
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(f'{name} ({email}): {message}')
        return render(request, 'restaurant/complain.html')

    def get(self, request):
        return render(request, 'restaurant/complain.html')


class InfoPageView(TemplateView):
    """Класс для отображения страницы с информацией о ресторане"""
    template_name = 'restaurant/info.html'

    def get(self, request):
        return render(request, 'restaurant/info.html')


class MenuPageView(TemplateView):
    """Класс для отображения страницы с информацией о ресторане"""
    template_name = 'restaurant/menu.html'

    def get(self, request):
        return render(request, 'restaurant/menu.html')


# def contact(request):
#     if request.method == 'POST':
#         """Метод для приема инфы с фронтэнда и ее вывода в консоль"""
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'{name} ({email}): {message}')
#     context = {'title': 'Контакты'}
#     return render(request, 'catalog/contact.html', context)

# def products_detail(request, pk):
#     """Метод для вывода товара по одному через его ID (primary key=pk)"""
#     product = get_object_or_404(Product, pk=pk)
#     context = {"products": product}
#     return render(request, 'product_detail.html', context)

# def index(request):
#     """Функция принимает параметр request (инфа от пользователя на фротэнде) и возвращает ответ"""
#     if request.method == "POST":
#         """В request хранится информация о методе, который отправлял пользователь"""
#         name = request.POST.get('name')
#         """И передается информация, которую заполнил пользователь"""
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'{name} ({email}): {message}')
#     return render(request, 'catalog/index.html')


def index(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return render(request, 'restaurant/booking_list.html')
        else:
            print("Ошибка в форме:", form.errors)  # Отладка ошибок формы
            return render(request, 'restaurant/booking_list.html', {'form': form})
    elif request.method == "GET":
        form = BookingForm()
        return render(request, 'restaurant/booking_list.html', {'form': form})
