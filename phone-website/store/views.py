from decimal import Decimal

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from .models import Product, SKU, CartItem, Order, OrderItem


# -------- helpers --------
def _get_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


# -------- pages --------
def product_list_clean(request):
    """Homepage list with search (brand dropdown + text)."""
    q = (request.GET.get("q") or "").strip()
    brand = (request.GET.get("brand") or "").strip()

    qs = Product.objects.all()
    if brand:
        qs = qs.filter(brand__icontains=brand)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    qs = qs.distinct()

    return render(
        request,
        "store/product_list.html",
        {"products": qs, "q": q, "brand": brand},
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "store/product_detail.html", {"product": product})


def view_cart(request):
    session_key = _get_session_key(request)
    items = (
        CartItem.objects
        .filter(session_key=session_key)
        .select_related("sku", "sku__product", "sku__price")
    )
    subtotal = Decimal("0.00")
    for it in items:
        unit = it.sku.price.sale_price or it.sku.price.list_price
        subtotal += unit * it.quantity
    return render(request, "store/cart.html", {"items": items, "subtotal": subtotal})


@require_POST
def add_to_cart(request, sku_id):
    session_key = _get_session_key(request)
    sku = get_object_or_404(SKU, pk=sku_id)
    item, created = CartItem.objects.get_or_create(
        session_key=session_key, sku=sku, defaults={"quantity": 1}
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect("view_cart")


@require_POST
def remove_from_cart(request, item_id):
    CartItem.objects.filter(pk=item_id).delete()
    return redirect("view_cart")


@require_POST
def checkout(request):
    session_key = _get_session_key(request)
    items = list(
        CartItem.objects
        .filter(session_key=session_key)
        .select_related("sku", "sku__price", "sku__inventory")
    )
    if not items:
        return redirect("product_list")

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        status="PAID",
    )
    total = Decimal("0.00")
    for it in items:
        price = it.sku.price.sale_price or it.sku.price.list_price
        OrderItem.objects.create(
            order=order, sku=it.sku, quantity=it.quantity, unit_price=price
        )
        total += price * it.quantity

        inv = getattr(it.sku, "inventory", None)
        if inv:
            inv.qty_on_hand = max(0, inv.qty_on_hand - it.quantity)
            inv.save()

    order.total = total
    order.save()

    CartItem.objects.filter(session_key=session_key).delete()
    return render(request, "store/order_success.html", {"order": order})


# -------- minimal JSON API (optional) --------
def api_products(request):
    data = [
        {
            "id": p.id,
            "name": p.name,
            "brand": p.brand,
            "skus": [
                {
                    "id": s.id,
                    "sku_code": s.sku_code,
                    "color": s.color,
                    "storage": s.storage,
                    "price": float(s.price.sale_price or s.price.list_price),
                }
                for s in p.skus.select_related("price").all()
            ],
        }
        for p in Product.objects.all()
    ]
    return JsonResponse(data, safe=False)


def api_product_detail(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    data = {
        "id": p.id,
        "name": p.name,
        "brand": p.brand,
        "description": p.description,
        "skus": [
            {
                "id": s.id,
                "sku_code": s.sku_code,
                "color": s.color,
                "storage": s.storage,
                "price": float(s.price.sale_price or s.price.list_price),
                "qty_on_hand": getattr(s, "inventory", None).qty_on_hand
                if hasattr(s, "inventory") else 0,
            }
            for s in p.skus.select_related("price", "inventory").all()
        ],
    }
    return JsonResponse(data)

