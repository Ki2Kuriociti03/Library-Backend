from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import BookSerializer, FavouriteSerializer, CreateFavouriteSerializer
from .models import Book, Favourite
from rest_framework import generics
from .models import User, Rating
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, RatingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


class FavouriteListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        favourites = Favourite.objects.filter(user=request.user)
        serializer = FavouriteSerializer(favourites, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CreateFavouriteSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.validated_data['book']
            Favourite.objects.get_or_create(user=request.user, book=book)
            return Response({"status": "book added to favourites successfully"}, status=201)
        return Response(serializer.errors, status=400)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny])
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/backend_api/token/',
        '/backend_api/register/',
        '/backend_api/token/refresh/'
    ]
    return Response(routes)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        response = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': response}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = "read!"
        response = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': response}, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)


class RatingListCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        book = request.data.get('book')
        rating = request.data.get('rating')

        if not book or not rating:
            raise ValidationError("Book ID and score are required")

        if Rating.objects.filter(user=user, book_id=book).exists():
            raise ValidationError("You have already rated this book")

        rating = Rating.objects.create(user=user, book_id=book, rating=rating)
        serializer = self.get_serializer(rating)
        return Response(serializer.data)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        book_id = self.request.query_params.get('book')
        if book_id:
            return Rating.objects.filter(book_id=book_id)
        return Rating.objects.none()


class BookView(APIView):
    def get(self, request, *args, **kwargs):

        id = request.query_params.get('id')
        if id is not None:
            book = Book.objects.get(id=id)
            output = [
                {
                    "id": book.id,
                    "name": book.name,
                    "author": book.author,
                    "year": book.year,
                    "isbn": book.isbn,
                    "quantity": book.quantity,
                    "tags": book.tags,
                    "image": f'{str(book.image)}'
                }
            ]
            return Response(output)
        else:
            output = [
                {
                    "id": output.id,
                    "name": output.name,
                    "author": output.author,
                    "year": output.year,
                    "isbn": output.isbn,
                    "quantity": output.quantity,
                    "tags": output.tags,
                    "image": f'{str(output.image)}'
                } for output in Book.objects.all()
            ]
            return Response(output)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        try:
            obj = Book.objects.get(pk=pk)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response(self, status=status.HTTP_404_NOT_FOUND)

