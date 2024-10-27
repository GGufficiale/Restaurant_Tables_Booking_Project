from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pytils.translit import slugify

from restaurant.forms import ProductForm, VersionForm, ProductModeratorForm
from restaurant.models import Product, Version
from restaurant.services import get_products_from_cache


# def product_list(request):
#     """Функция принимает параметр request (инфа от пользователя на фротэнде) и возвращает ответ"""
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, 'products_list.html', context)

class ProductListView(ListView):
    """Класс, заменяющий функцию product_list (FBV на CBV)"""
    model = Product

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(DetailView):
    """Класс, заменяющий функцию products_detail (FBV на CBV)"""
    model = Product

    def get_object(self, queryset=None):
        """Метод для подсчета к-ва просмотров страницы"""
        self.object = super().get_object()
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        """Метод для отправки пользователю ссылки на почту при верификации почты"""
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    # """Метод для отображения латиницей кириллических названий товара"""
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.name)
    #         new_mat.save()
    #     return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.name)
    #         new_mat.save()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:products_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormSet = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        """Метод для добавления новых версий товара"""
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        """Метод для работы с правами доступа"""
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('product.can_cancel_publication') and user.has_perm(
                'product.can_edit_description') and user.has_perm('product.can_change_category'):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')

    def get_object(self, queryset=None):
        """Метод для определения доступа к удалению только своих товаров"""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            self.object.save()
            return self.object
        raise PermissionDenied


def toggle_activity(request, pk):
    """Функция-контроллер для изменения статуса активности товара"""
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_published:
        product_item.is_published = False
    else:
        product_item.is_published = True
    product_item.save()
    return redirect(reverse('catalog:products_list'))


class ContactPageView(TemplateView):
    """Класс для отображения страницы с контактами"""
    template_name = 'catalog/contact.html'

    def post(self, request, *args, **kwargs):
        """Метод для приема инфы с фронтэнда в контактах и ее вывода в консоль"""
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(f'{name} ({email}): {message}')
        return render(request, 'catalog/contact.html')

    def get(self, request):
        return render(request, 'catalog/contact.html')

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
