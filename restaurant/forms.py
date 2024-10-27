from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from restaurant.models import Product, Version


class StyleFormMixin:
    """Стилизация для формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        # Строка для исключения поля. Если нужно вывести все - пишем "__all__"
        exclude = ("views_counter", 'owner')

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise ValidationError(f'Наименование не должно содержать слово "{forbidden_word}"')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for forbidden_word in self.forbidden_words:
            if forbidden_word in cleaned_data.lower():
                raise ValidationError(f'Описание не должно содержать слово "{forbidden_word}"')
        return cleaned_data


class ProductModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        # Строка для исключения поля. Если нужно вывести все - пишем "__all__"
        fields = ("description", 'category')


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        # Строка для исключения поля. Если нужно вывести все - пишем "__all__"
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        is_version_active = cleaned_data.get('is_version_active')
        if is_version_active:
            active_versions = Version.objects.filter(is_version_active=True)
            if self.instance.pk:
                active_versions = active_versions.exclude(pk=self.instance.pk)
            if active_versions.exists():
                raise ValidationError("Может быть только одна активная версия.")
        return cleaned_data
