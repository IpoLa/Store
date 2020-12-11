from django import forms
from .models import Order
from products.models import Product

class OrderForm(forms.ModelForm):
    shipping_address = forms.CharField(label="",
        required=False,
        widget=forms.Textarea(
        attrs={
            "class": "shipping_address_class",
            "rows": "3",
            "placeholder": "Your shipping address",
        }
    ))
    billing_address = forms.CharField(label="",
        widget=forms.Textarea(
        attrs={
            "class": "billing_address_class",
            "rows": "3",
            "placeholder": "Your billing address",
        }
    ))
    def __init__(self, *args, **kwargs):
        product = kwargs.pop("product") or None
        super().__init__(*args, **kwargs)
        self.product = product

    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'billing_address',
        ]
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        shipping_addr = cleaned_data.get("shipping_address")
        # Check product inventory 
        if self.product != None:
            if not self.product.can_order:
                raise forms.ValidationError("This product cannot be ordered at this time.")
            if (self.product.requires_shipping and shipping_addr == "") or (self.product.requires_shipping and shipping_addr == None):
                self.add_error("shipping_address", "Please enter your shipping address.")
        return cleaned_data