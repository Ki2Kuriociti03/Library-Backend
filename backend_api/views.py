from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import BookSerializer
from .models import Book
from rest_framework import generics
from .models import Profile, User
from .serializer import UserSerializer, MyTokenObtainPairSerializer,RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == 'GET':
        response = f'{request.user} seeing a GET response'
        return Response({'response': response}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        response = f'{request.user}, your text is: {text}'
        return Response({'response': response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)



class BookView(APIView):
    def get(self, request):
        output = [
            {
                "name": output.name,
                "author": output.author,
                "year": output.year,
                "rating": output.rating,
                "isbn": output.isbn,
                "quantity": output.quantity,
                "tags": output.tags
            } for output in Book.objects.all()
        ]
        return Response(output)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)