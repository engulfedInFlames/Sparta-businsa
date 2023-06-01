from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from inbound.models import Inbound
from inbound.forms import InboundForm
from outbound.models import Outbound
from outbound.forms import OutboundForm
from .forms import ProductRegisterForm


def home(request):
    # Home
    all_products = Product.objects.all()
    return render(request, "products/home.html", {"products": all_products})


def detail_view(request, _id):
    product = Product.objects.get(id=_id)
    return render(request, "products/detail.html", {"product": product})


@login_required
def register(request):
    if request.method == "GET":
        form = ProductRegisterForm()
        return render(request, "products/register.html", {"form": form})

    if request.method == "POST":
        form = ProductRegisterForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)

            """ 14digit Product Code Classification """

            type = form.cleaned_data.get("type")
            color = form.cleaned_data.get("color")
            size = form.cleaned_data.get("size")
            number_of_registered_products = len(Product.objects.all())
            code = type + color + size + f"{number_of_registered_products}".zfill(6)
            product.code = code
            product.user = request.user
            product.save()

    return redirect(f"/profile/{request.user.id}")


@login_required
def delete(request, _id):
    user = request.user
    Product.objects.get(id=_id).delete()
    return redirect(f"/profile/{user.id}")


@login_required
def inventory_view(request, _id):
    all_inbound = Inbound.objects.all().filter(user_id=_id)
    all_outbound = Outbound.objects.all().filter(user_id=_id)

    return render(
        request,
        "inventory/inventory.html",
        {"inbounds": all_inbound, "outbounds": all_outbound},
    )


# tranjaction.atomic
@login_required
def inbound(request, _id):
    if request.method == "GET":
        form = InboundForm(_id)
        products = Product.objects.all().filter(user_id=_id)

        now = datetime.now().strftime("%Y-%m-%d")
        return render(
            request,
            "inventory/inbound.html",
            {"today": now, "products": products, "form": form},
        )

    if request.method == "POST":
        user = request.user

        code = request.POST.get("code", "")
        product = Product.objects.get(code=code)
        quantity = int(request.POST.get("quantity", 0))
        total_price = int(request.POST.get("unit-price", 0)) * quantity
        date = request.POST.get("inbound-date", "")

        try:
            inbound = Inbound(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
                inbound_date=date,
            )
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
        return render(
            request, "inventory/outbound.html", {"today": now, "products": products}
        )

    if request.method == "POST":
        user = request.user

        code = request.POST.get("code", "")
        product = Product.objects.get(code=code)
        quantity = int(request.POST.get("quantity", 0))
        total_price = int(product.price) * quantity
        date = request.POST.get("outbound-date", "")

        if product.stock < quantity:
            return render(
                request,
                "inventory/outbound.html",
                {"error": "출고 수량이 재고 수량보다 많습니다.", "today": now, "products": products},
            )

        try:
            outbound = Outbound(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
                outbound_date=date,
            )
            outbound.save()
            product.stock -= quantity
            product.save()
        except Outbound.DoesNotExist:
            return render(request, "inventory/outbound.html", {"error": "입력이 잘못됐습니다."})

    return redirect(f"/products/{_id}/inventory")


@login_required
def order(request):
    return render(request, "products/order.html")
