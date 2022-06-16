from django.urls import path, include
from .views import UserRegistrationView, UserLogin, Profile, UserChangePasswordView
from .views import PassengerViewSet, BookingDetailsViewSet, FlightViewSet
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'flight', FlightViewSet)
routers.register(r'bookingdetails', BookingDetailsViewSet, basename="booking")
routers.register(r'passenger', PassengerViewSet)

urlpatterns = [
    path('', include(routers.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),

]


