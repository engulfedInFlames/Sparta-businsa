from django import forms
from outbound.models import Outbound
from products.models import Product


class OutboundForm(forms.ModelForm):
    """ModelForm For Outbound"""

    # class Meta:
    #     model = Outbound
    #     fields = ("name", "price", "type", "color", "size")
    #     labels = {
    #         "name": "상품명",
    #         "price": "상품 가격",
    #     }
    #     # help_texts = {}

    #     widgets = {
    #         "name": forms.TextInput(attrs={"class": "form-control"}),
    #         "price": forms.NumberInput(attrs={"class": "form-control"}),
    #     }

    # def clean(self):
    #     data = super().clean()
    #     try:
    #         if all(data.values()):
    #             return data
    #         raise forms.ValidationError("양식을 모두 채워주세요.")

    #     except forms.ValidationError as e:
    #         print(e)
