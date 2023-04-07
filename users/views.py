from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from products.models import Product


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'users/signin.html', {'error': '아이디와 비밀번호는 반드시 입력해야 합니다.'})

        # makemigrations - migrate를 통해 User 모델은 DB와 연결된 상태이다.
        exist_user = auth.authenticate(
            request, username=username, password=password)
        if exist_user:
            # ↓ django에서 다음의 역할을 수행하도록 하는 명령어 : request.session['user'] = exist_user.username
            auth.login(request, exist_user)
            return redirect("/")

        return render(request, 'users/signin.html', {'error': '아이디 또는 비밀번호가 잘못 입력됐습니다.'})

    user = request.user.is_authenticated

    if user:
        return redirect('/')

    return render(request, 'users/signin.html')


def signup(request):

    if request.method == "POST":
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")
        gender = request.POST.get("gender", "")

        exist_user = get_user_model().objects.filter(username=username)
        if exist_user:
            return render(request, 'users/signup.html', {'error': '존재하는 계정입니다'})

        if password != password2:
            # 비밀번호를 제대로 입력하지 않았을 때때
            return render(request, 'users/signup.html', {'error': '비밀번호를 정확히 입력하세요.'})

        if not username or not password:
            return render(request, 'users/signup.html', {'error': '사용자 이름과 비밀번호는 반드시 입력해야 합니다.'})

        CustomUser.objects.create_user(
            email=email, username=username, password=password, gender=gender)
        return render(request, "users/signin.html")

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, "users/signup.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/sign-in/")


@login_required
def show_profile(request, _id):
    if request.method == "GET":
        all_products = Product.objects.filter(user_id=_id)
        return render(request, "users/profile.html", {"products": all_products})

    return redirect("/")
