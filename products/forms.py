from django import forms
from .models import Product


class ProductRegisterForm(forms.ModelForm):

    """ModelForm For Product Register"""

    TypeChoices = (
        ("01", "상의"),
        ("02", "아우터"),
        ("03", "원피스"),
        ("04", "하의"),
        ("05", "스커트"),
        ("06", "신발"),
        ("07", "가방"),
        ("08", "악세사리"),
    )
    ColorChoices = (
        ("01", "흰색"),
        ("02", "검정색"),
        ("03", "빨간색"),
        ("04", "주황색"),
        ("05", "노란색"),
        ("06", "초록색"),
        ("07", "파란색"),
        ("08", "남색"),
        ("09", "보라색"),
    )
    SizeChoices = (
        ("SS", "SS"),
        ("NS", "S"),
        ("NM", "M"),
        ("NL", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    )

    type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=TypeChoices,
        label="품목",
        required=True,
    )
    color = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=ColorChoices,
        label="색상",
        required=True,
    )
    size = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=SizeChoices,
        label="크기",
        required=True,
    )

    class Meta:
        model = Product
        fields = ("name", "price", "type", "color", "size")
        labels = {
            "name": "상품명",
            "price": "상품 가격",
        }
        # help_texts = {}

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        data = super().clean()
        try:
            if all(data.values()):
                return data
            raise forms.ValidationError("양식을 모두 채워주세요.")

        except forms.ValidationError as e:
            print(e)
