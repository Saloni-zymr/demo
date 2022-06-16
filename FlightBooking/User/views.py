from .models import User, Flight, BookingDetails, Passenger
from .renderers import UserRenderer
from .serializers import UserRegistrationSerializer, LoginSerializer, ProfileViewSerializer, \
    UserChangePasswordSerializer, FlightSerializer, BookingDetailsSerializer, PassengerSerializer
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, formate=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request, formate=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password id not valid']}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileViewSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, formate=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class BookingDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = BookingDetails.objects.all()
    serializer_class = BookingDetailsSerializer

    def get_queryset(self):
        book = BookingDetails.objects.all()
        return book

    def create(self, request, *args, **kwargs):
        data = request.data

        user = User.objects.get(pk=data["u_id"])
        flightdetails = Flight.objects.get(pk=data["f_id"])

        new_book = BookingDetails.objects.create(
            trip_date=data["trip_date"],
            no_of_passengers=data["no_of_passengers"],
            price=flightdetails.price * len(data["passenger"]),
            u_id=user,
            f_id=flightdetails,
        )
        new_book.save()
        for passenger in data["passenger"]:
            p = Passenger.objects.create(
                name=passenger["name"],
                age=passenger["age"],
                gender=passenger["gender"],
                contact=passenger["contact"],
                u_id=user,
            )
            new_book.passenger.add(p)

        if flightdetails.avail_seats < len(data["passenger"]):
            return Response({"data": "No seats available", "status": status.HTTP_400_BAD_REQUEST})
        update_seats = flightdetails.avail_seats - data["no_of_passengers"]
        flightdetails.avail_seats = update_seats
        flightdetails.save()
        serializers = BookingDetailsSerializer(new_book)
        return Response({"data": serializers.data, "status": status.HTTP_201_CREATED})


class PassengerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
