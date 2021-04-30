from itertools import chain
from django.contrib.auth.models import User
from .models import UserData, Item

def generate_mock_data():
    try:
        print('Generating mock data...')
        if (User.objects.filter(username='admin').exists() == False and
            User.objects.filter(username='user1').exists() == False and
                User.objects.filter(username='user2').exists() == False):

            user = User.objects.create_user('admin', 'admin@admin.admin', 'admin')
            user.is_superuser = True
            user.save()
            userData = UserData(funds='1000', reserved_funds=0)
            userData.user = user
            userData.save()

            item = Item(name='Auction Item 1', starting_price=500, current_bid=500,
                        min_increment=500, location='Location 1', expiration_time='2021-12-12 12:12+00:00')
            item.owner = user
            item.bidder = user
            item.save()

            user = User.objects.create_user('user1', 'user1@user1.user1', 'user1')
            userData = UserData(funds='1800', reserved_funds=0)
            userData.user = user
            userData.save()

            item = Item(name='Auction Item 2', starting_price=100, current_bid=100,
                        min_increment=50, location='Location 2', expiration_time='2022-12-12 12:12+00:00')
            item.owner = user
            item.bidder = user
            item.save()

            user = User.objects.create_user('user2', 'user2@user2.user2', 'user2')
            userData = UserData(funds='1200', reserved_funds=0)
            userData.user = user
            userData.save()

            item = Item(name='Auction Item 3', starting_price=200, current_bid=200,
                        min_increment=50, location='Location 3', expiration_time='2024-12-12 12:12+00:00')
            item.owner = user
            item.bidder = user
            item.save()
    except:
        print("Mock data was not generated")

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data
