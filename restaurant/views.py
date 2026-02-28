from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, UserSerializer


# ─────────────────────────────────────────
#  HTML Views (Static Pages)
# ─────────────────────────────────────────

def index(request):
    return render(request, 'restaurant/index.html', {'title': 'Little Lemon'})


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'About'})


def menu(request):
    menu_items = Menu.objects.all()
    return render(request, 'restaurant/menu.html', {
        'title': 'Menu',
        'menu_items': menu_items,
    })


def book(request):
    return render(request, 'restaurant/book.html', {'title': 'Book a Table'})


# ─────────────────────────────────────────
#  Menu API
# ─────────────────────────────────────────

class MenuItemView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


# ─────────────────────────────────────────
#  Booking API
# ─────────────────────────────────────────

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


# ─────────────────────────────────────────
#  User Registration & Auth
# ─────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    """
    Register a new user and return token.
    POST /api/registration/
    Body: { username, password, email, first_name, last_name }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
    }, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login and receive token.
    POST /api/login/
    Body: { username, password }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})
    return Response({'error': 'Invalid credentials.'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    GET /api/me/  → Returns current authenticated user info.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
