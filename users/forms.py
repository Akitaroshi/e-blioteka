from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser

INPUT_CLASS = (
    'w-full px-4 py-2.5 border border-slate-200 rounded-xl '
    'focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 '
    'outline-none transition duration-200 bg-white'
)


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=150)
    phone = forms.CharField(
        label='Телефон',
        max_length=16,
        widget=forms.TextInput(attrs={
            'data-phone-mask': 'true',
        }),
    )
    email = forms.EmailField(label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'phone', 'email')
        help_texts = {
            'username': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = INPUT_CLASS
            if field_name == 'username':
                field.widget.attrs['data-username-field'] = 'true'
            if field_name == 'password1':
                field.widget.attrs['data-password-field'] = 'true'
            if field_name == 'phone':
                field.widget.attrs.setdefault('data-phone-mask', 'true')

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.fullmatch(r'[А-Яа-яЁё\s]+', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы')
        return full_name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.fullmatch(r'8\(\d{3}\)\d{3}-\d{2}-\d{2}', phone):
            raise ValidationError('Введите телефон полностью в формате 8(XXX)XXX-XX-XX')
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = INPUT_CLASS
