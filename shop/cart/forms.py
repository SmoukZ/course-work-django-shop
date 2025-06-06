# cart/forms.py
from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            # Динамически заполняем доступные размеры
            sizes = product.get_sizes_list()
            self.fields['size'].choices = [(size, size) for size in sizes]
            if not sizes:
                self.fields['size'].required = False  # Если размеров нет, поле необязательное

    def clean(self):
        cleaned_data = super().clean()
        size = cleaned_data.get('size')
        if self.fields['size'].required and not size:
            raise forms.ValidationError("Пожалуйста, выберите размер.")
        return cleaned_data