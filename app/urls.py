
from django.urls import include, path
from app import views

urlpatterns = [
    path('', views.Index, name='Index'),
    path('category/<slug>', views.ByCategory, name='Category'),
    path('search/<name>', views.BySearch, name='Category'),
    path('about', views.AbouUs, name='About'),
    path('team', views.Team, name='Team'),
    path('contact/', views.HandleContact, name='Contact'),
    path('cart/', views.Cart, name="Cart"),
    path('checkout/', views.Checkout, name="checkout"),
    path('callback/', views.Callback, name="Cart"),
]
