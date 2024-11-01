from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField, DateTimeInput
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
            'datetime_booking': DateTimeInput(
                format='%Y-%m-%dT%H:%M',  # формат для datetime-local
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date and time',
                       'type': 'datetime-local'
                       }),
        }

    def clean_datetime_booking(self):
        datetime_booking = self.cleaned_data['datetime_booking']
        booking_time = datetime_booking.time()
        # Проверяем, что часы в диапазоне от 12 до 23
        if not (12 <= booking_time.hour <= 23):
            raise ValidationError("Выберите время с 12:00 до 23:00.")
        # Проверяем, что минуты равны 00, 15, 30 или 45
        if booking_time.minute not in {0, 15, 30, 45}:
            raise ValidationError("Минуты должны быть 00, 15, 30 или 45.")
        return datetime_booking

    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция",
                       "радар"]

    # def clean_availability_check(self):
    #     date_to_check = self.cleaned_data['datetime_booking']
    #     exists = Booking.objects.filter(datetime_booking=date_to_check).exists()
    #     if exists:
    #         raise ValidationError("Данная дата уже существует в базе данных.")

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
