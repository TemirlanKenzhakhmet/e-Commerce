from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.contrib import messages
from django.views.generic import View

from .models import Item, Category, Order, OrderItem, BillingAddress
from .forms import NewItemForm, EditItemForm, CheckoutForm
 

def detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(slug=slug)[:4]
    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'item/detail.html', context)
    

def search_list(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    return render(request, 'item/search.html', {
        'items': items,
        'categories': categories,
    })

def search_results(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    items = Item.objects.filter(is_sold=False)
    if category_id:
        items = items.filter(category_id=category_id)
        
    if query:
        items = items.search(query=query)
    
    return render(request, 'item/partials/results.html', {
        'items': items,
    })




@login_required
def create(request): 
    if request.method == "POST":
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', slug=item.slug)
    else: 
        form = NewItemForm()

    return render(request, 'item/create.html', {
        'form': form,
        'title': 'New item',
    })


@login_required
def edit(request, slug): 
    item = get_object_or_404(Item, slug=slug, created_by=request.user)
    if request.method == "POST":
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', slug=item.slug)
    else: 
        form = EditItemForm(instance=item)

    return render(request, 'item/create.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, slug):
    item = get_object_or_404(Item, slug=slug, created_by=request.user)
    item.delete()
    return redirect('dashboard:index')


# ------------------------------------------------------------------------------------------------------------------------------- #


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, "The quantity of this item was increased.")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
    return redirect('item:detail', slug=slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
        else:
            messages.info(request, "This item was not in your cart.")

    else:
        messages.info(request, "You do not have an active order.")
    return redirect('item:detail', slug=slug)


@login_required
def remove_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
    if order_item.quantity > 1:
        order_item.quantity = F('quantity') - 1
        order_item.save()
        messages.info(request, "The quantity of this item was decreased.")
    else:
        order_item.delete()
        messages.info(request, "This item was removed from your cart.")
        
    return redirect('item:order-summary')


@login_required
def add_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get(item=item, user=request.user, ordered=False)

    order_item.quantity = F('quantity') + 1
    order_item.save()
    messages.info(request, "The quantity of this item was increased.")

    return redirect('item:order-summary')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order, 
            }
            return render(self.request, 'item/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order.')
            return redirect('/')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form, 
        }
        return render(self.request, 'item/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                same_shipping_address = form.cleaned_data.get('same_shipping_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip_code = zip_code,
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('item:payment')
            messages.warning(self.request, 'Failed checkout.')
            return redirect('item:checkout')
        
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order.')
            return redirect('/')


class PaymentView(View):
    # TODO something, I`m gonna do lately`
    def get(self, *args, **kwargs):
        return render(self.request, 'item/payment.html')