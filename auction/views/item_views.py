from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import models, transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import Item, UserData
from ..forms import AddItemForm
from ..utils import to_dict


@login_required
def add_item_view(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            starting_price = request.POST.get('starting_price')
            min_increment = request.POST.get('min_increment')
            location = request.POST.get('location')
            expiration_time = request.POST.get('expiration_time')
            expiration_time_converted = datetime.strptime(
                expiration_time, '%a, %d %b %Y %H:%M %Z%z').isoformat()
            item = Item(name=name, starting_price=starting_price, current_bid=starting_price,
                        min_increment=min_increment, location=location, expiration_time=expiration_time_converted)
            user = User.objects.get(id=request.user.id)
            if user is not None:
                item.owner = user
                item.bidder = user
                item.save()
                messages.success(request, 'Your item has been listed.')
                return redirect(to='/items')
            else:
                messages.error(request, 'Unknown error.')
                return redirect(to='/item/add')
        else:
            messages.error(request, 'Validation failed.')
            return redirect(to='/items')
    else:
        form = AddItemForm()
        return TemplateResponse(request, 'items/add_item.html', {'form': form})


@transaction.non_atomic_requests
def items_view(request):
    # Money is never transferred if there are no visitors
    update_auctions(request.user.id)

    if request.method == 'POST':
        # Vulnerability (should check if bids can be made
        # for the item)
        id = request.POST.get('id')
        bid = request.POST.get('bid')
        item = Item.objects.get(id=id)
        user_data = UserData.objects.get(user_id=request.user.id)
        if user_data.funds - user_data.reserved_funds < int(bid):
            messages.error(request, 'Insufficient funds.')
            return redirect('/items')
        item.bidder_id = request.user.id
        # Vulnerability (no check whether bid is allowed,
        # e.g. own items should not be biddable)
        item.current_bid = bid
        item.save()
        calculate_reserved_funds(item.owner_id)
        calculate_reserved_funds(item.bidder_id)
        messages.success(
            request, 'You are now the highest bidder for the item.')
        return redirect('/items')
    else:
        items = Item.objects.all()
        user_data = UserData.objects.get(user_id=request.user.id)
        for x in items:
            x.next_min_bid = x.current_bid + x.min_increment
            if user_data.funds - user_data.reserved_funds >= int(x.next_min_bid):
                x.can_bid = True

        # Vulnerability (all owner&bidder info passed)
        return TemplateResponse(request, 'items/items.html', {'items': items})


@transaction.non_atomic_requests
@login_required
def delete_item_view(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # Vulnerability (The value is received from a hidden
        # input field in the form in the page. However, this
        # value can be changed by an attacker.
        # Request.user.id should be used instead.)
        userId = request.POST.get('userId')
        item = Item.objects.get(id=id)
        # Vulnerability (any user named "admin" can delete items)
        if item.owner.id == int(userId) or request.user.username == 'admin':
            item.delete()
            calculate_reserved_funds(item.owner_id)
            calculate_reserved_funds(item.bidder_id)
            messages.success(request, 'The item has been unlisted.')
            return redirect('/items')
        else:
            return redirect('/unauthorized')
    else:
        return redirect('/items')


@transaction.non_atomic_requests
def update_auctions(user_id):
    items = Item.objects.filter(expiration_time__lte=timezone.now())

    for x in items:
        bidder_data = UserData.objects.get(user=x.bidder)
        bidder_data.funds -= x.current_bid
        bidder_data.reserved_funds += x.current_bid
        bidder_data.save()

        owner_data = UserData.objects.get(user=x.owner)
        owner_data.funds += x.current_bid
        owner_data.reserved_funds -= x.current_bid
        owner_data.save()

        x.delete()

        print('Auction for "' + x.name + '" completed')


def calculate_reserved_funds(user_id):
    user_data = UserData.objects.get(user_id=user_id)
    items = Item.objects.filter(bidder_id=user_id)
    total = 0
    for x in items:
        total += x.current_bid
    user_data.reserved_funds = total
    user_data.save()
