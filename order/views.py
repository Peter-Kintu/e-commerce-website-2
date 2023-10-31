import json
import stripe

from django.conf import settings
from django.http import JsonResponse

from cart.cart import Cart

from .models import Order, OrderItem

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])

        items.append( {
            'price_data': {
                'currency': 'Ugx',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.price,

            },
            'quantity': item['quantity']
        })


    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='https://127.0.0.1:8000/cart/success',
        cancel_url='https://127.0.0.1:8000/cart/'
    )
    payment_intent = session.payment_intent

    order = Order.objects.create(
        user=request.user,
        first_name=data['first_name'],
        last_name= data['last_name'],
        email=data['email'],
        address=data['address'],
        zipcode=data['zipcode'],
        place=data['place'],
        phone=data['phone'],
        payment_intent=payment_intent,
        pay=True,
        paid_amount=total_price
        )
    
    for item in cart:
        product = item['product']
        quantity = int(item['qauntity'])
        price = product.price * qauntity
            
        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})