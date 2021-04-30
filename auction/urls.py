from django.urls import path
from .views import homepage_view, logs_view
from .views.auth_views import login_view, logout_view, unauthorized_view
from .views.user_views import users_view, register_view
from .views.item_views import add_item_view, items_view, delete_item_view
from .utils import generate_mock_data

urlpatterns = [
    path('', homepage_view, name='home'),
    path('items/add', add_item_view, name='list'),
    path('items/delete', delete_item_view, name='delete'),
    path('items', items_view, name='items'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('users', users_view, name='user'),
    path('register', register_view, name='register'),
    path('logs', logs_view, name='logs'),
    path('unauthorized', unauthorized_view, name='unauthorized'),
]

generate_mock_data()
