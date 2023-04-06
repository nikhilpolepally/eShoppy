
from django.urls import include, path
from userAuth import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.userLogin,name='handlelogin'),
    path('logout/',views.Userlogout,name='handlelogout'),
    path('', include('social_django.urls', namespace='social')),
]
