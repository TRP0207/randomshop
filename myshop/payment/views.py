from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import braintree
from orders.models import Order
from .tasks import payment_completed
# Create your views here.
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = Order.get_total_cost(self=order)

    if request.method == 'POST':
        #retrive nounce
        nounce = request.POST.get('payment_method_nonce', None)
        #create and submit transactions
        result = gateway.transaction.sale({
                'amount': f'{total_cost:.2f}',
                'payment_method_nonce': nounce,
                'options': {
                    'submit_for_settlement': True}
        })
        if result.is_success:
            #mark the order as paid
            order.paid = True
            #store the unique transaction id
            order.braintree_id =result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return  redirect('payment:cancel')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        #retrive nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # craete and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost: .2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True,
            }
        })
        if result.is_success:
            #mark the order paid
            order.paid = True
            #store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            #launch asynchronous task
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        return render(request, 'payment/process.html',
                      {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')




