from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from products.models import Product
from users.forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 중복 저장 방지
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect("/sign-in")

        else:
            if form.errors:
                print(form.errors)
                return render(request, "users/signup.html", {"form": form})

    if request.user.is_authenticated:
        return redirect("/")

    form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if not username or not password:
            return render(
                request, "users/signin.html", {"error": "아이디와 비밀번호는 반드시 입력해야 합니다."}
            )

        # makemigrations - migrate를 통해 User 모델은 DB와 연결된 상태이다.
        exist_user = auth.authenticate(request, username=username, password=password)
        if exist_user:
            # ↓ django에서 다음의 역할을 수행하도록 하는 명령어 : request.session['user'] = exist_user.username
            auth.login(request, exist_user)
            return redirect("/")

        return render(
            request, "users/signin.html", {"error": "아이디 또는 비밀번호가 잘못 입력됐습니다."}
        )

    user = request.user.is_authenticated

    if user:
        return redirect("/")

    return render(request, "users/signin.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/sign-in/")


@login_required
def profile(request, _id):
    if request.method == "GET":
        all_products = Product.objects.filter(user_id=_id)
        return render(request, "users/profile.html", {"products": all_products})

    return redirect("/")
