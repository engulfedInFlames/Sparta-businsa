from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from inbound.models import Inbound
from outbound.models import Outbound


def home(request):
    # Home
    all_products = Product.objects.all()
    return render(request, "products/home.html", {"products": all_products})


def show_detail(request, _id):
    return render(request, "products/detail.html")


@login_required
def register(request):
    if request.method == "GET":
        return render(request, "products/register.html")

    user_id = None

    if request.method == "POST":
        user = request.user
        user_id = user.id

        name = request.POST.get("name", "")
        price = request.POST.get("price", "")

        type = request.POST.get("type", "")
        color = request.POST.get("color", "")
        size = request.POST.get("size", "")
        number_of_registered_products = len(Product.objects.all())
        code = type+color+size + f"{number_of_registered_products}".zfill(6)

        if all([user, name, price, type, color, size]):
            try:
                product = Product(user=user, name=name, price=price, code=code)
                product.save()
            except Product.DoesNotExist:
                return render(request, "products/register.html", {'error': '입력이 잘못됐습니다. 모든 칸을 채워주세요.'})

    return redirect(f"/profile/{user_id}")


@login_required
def delete(request, _id):
    user = request.user
    Product.objects.get(id=_id).delete()
    return redirect(f"/profile/{user.id}")


@login_required
def inventory(request, _id):
    all_inbound = Inbound.objects.all().filter(user_id=_id)
    all_outbound = Outbound.objects.all().filter(user_id=_id)

    return render(request, "inventory/inventory.html", {"inbounds": all_inbound, "outbounds": all_outbound})


@login_required
def inbound(request, _id):
    if request.method == "GET":
        products = Product.objects.all().filter(user_id=_id)

        now = datetime.now().strftime("%Y-%m-%d")
        return render(request, "inventory/inbound.html", {"today": now, "products": products})

    if request.method == "POST":
        user = request.user

        code = request.POST.get("code", "")
        product = Product.objects.get(code=code)
        quantity = int(request.POST.get("quantity", 0))
        total_price = int(request.POST.get("unit-price", 0)) * quantity
        date = request.POST.get("inbound-date", "")

        try:
            inbound = Inbound(user=user, product=product, quantity=quantity,
                              total_price=total_price, inbound_date=date)
            inbound.save()
            product.stock += quantity
            product.save()
        except Inbound.DoesNotExist:
            return render(request, "inventory/inbound.html", {"error": "입력이 잘못됐습니다."})

    return redirect(f"/products/{_id}/inventory")


@login_required
def outbound(request, _id):
    products = Product.objects.all().filter(user_id=_id)
    now = datetime.now().strftime("%Y-%m-%d")

    if request.method == "GET":

        return render(request, "inventory/outbound.html", {"today": now, "products": products})

    if request.method == "POST":
        user = request.user

        code = request.POST.get("code", "")
        product = Product.objects.get(code=code)
        quantity = int(request.POST.get("quantity", 0))
        total_price = int(product.price) * quantity
        date = request.POST.get("outbound-date", "")

        if product.stock < quantity:
            return render(request, "inventory/outbound.html", {"error": "출고 수량이 재고 수량보다 많습니다.", "today": now, "products": products})

        try:
            outbound = Outbound(user=user, product=product, quantity=quantity,
                                total_price=total_price, outbound_date=date)
            outbound.save()
            product.stock -= quantity
            product.save()
        except Outbound.DoesNotExist:
            return render(request, "inventory/outbound.html", {"error": "입력이 잘못됐습니다."})

    return redirect(f"/products/{_id}/inventory")


@ login_required
def order(request):
    return render(request, "products/order.html")
