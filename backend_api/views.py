from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import BookSerializer
from .models import Book


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