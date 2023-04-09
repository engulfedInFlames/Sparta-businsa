from django import forms
from .models import CustomUser


class SignupForm(forms.ModelForm):
    GenderChoices = (
        ("male", "남성"),
        ("female", "여성"),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
        label="비밀번호",
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control"}
        ),
        label="비밀번호 확인",
        required=True
    )
    gender = forms.ChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control"}
        ),
        choices=GenderChoices,
        label="성별",
        required=True
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "gender",
            "email",
        )
        labels = {
            "username": "이름",
            "email": "이메일",
        }
        help_texts = {
            "username": "",
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "gender": forms.Select(attrs={
                "class": "form-control"
            }),
        }

    def clean(self):
        data = super().clean()
        password1 = data.get("password1")
        password2 = data.get("password2")

        try:
            if password1 != password2:
                raise forms.ValidationError(
                    {"password2": ["비밀번호가 일치하지 않습니다.",]}
                )
        except forms.ValidationError as e:
            print(f"Password Validation Error: {e}")

        username = data.get("username")
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return data
        raise forms.ValidationError(
            {"username": ["존재하는 아이디입니다."]}
        )
