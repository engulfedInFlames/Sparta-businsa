from django import forms
from inbound.models import Inbound
from products.models import Product


class InboundForm(forms.ModelForm):
    """ModelForm For Inbound"""

    codes = []

    price_per = forms.CharField(
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        label="단위 가격 (개당 가격)",
        required=True,
    )

    code = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=codes,
        required=True,
    )

    def __init__(self, user_id, *args, **kwargs):
        self.user_id = user_id
        self.products = Product.objects.all().filter(id=self.user_id)
        self.codes = [(product.name, product.code) for product in self.products]
        super().__init__(*args, **kwargs)
        self.fields["code"].choices = self.codes

    class Meta:
        model = Inbound
        fields = ("code", "quantity", "price_per", "date")
        labels = {
            "code": "입고할 상품",
            "quantity": "수량",
            "date": "입고 예정 날짜",
        }
        # help_texts = {}

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        data = super().clean()
        try:
            if all(data.values()):
                return data
            raise forms.ValidationError("양식을 모두 채워주세요.")

        except forms.ValidationError as e:
            print(e)
