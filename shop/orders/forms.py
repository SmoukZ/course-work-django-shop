from django import forms
from .models import Order
import re

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'phone_number']
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            # Проверка формата номера телефона (пример: +79991234567 или 89991234567)
            if not re.match(r'^\+?\d{10,15}$', phone_number):
                raise forms.ValidationError('Введите корректный номер телефона (например, +79991234567).')
        return phone_number

    
    def save(self, commit=True):
        order = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            order.user = self.request.user
        else:
            order.user = None
        if commit:
            order.save()
        return order