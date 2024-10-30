from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, DateInput, DateTimeInput

from restaurant.models import Table, Booking


class StyleFormMixin:
    """Стилизация для формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BookingForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Booking
        # Строка для исключения поля. Если нужно вывести все - пишем "__all__"
        exclude = ("views_counter", 'owner')
        widgets = {
            'datetime_booking': DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date and time',
                       'type': 'date'
                       }),
        }

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


class BookingModeratorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Booking
        # Строка для исключения поля. Если нужно вывести все - пишем "__all__"
        fields = ("description", 'owner')
