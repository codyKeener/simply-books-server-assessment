from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import BookGenre, Book, Genre


class BookGenreView(ViewSet):
  
  # GENRES ARE NOT LOCKED BEHIND UIDS BECAUSE THEY WILL BE PROVIDED BY SIMPLY BOOKS AND NOT EDITABLE BY THE USERS

    def retrieve(self, request, pk):
      try:
          bookGenre = BookGenre.objects.get(pk=pk)
          serializer = BookGenreSerializer(bookGenre)
          return Response(serializer.data)
      except BookGenre.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
      try:
        bookGenres = BookGenre.objects.all()
    
        serializer = BookGenreSerializer(bookGenres, many=True)
        return Response(serializer.data)
      except:
        return Response({'message': 'Check query'}, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request):
      bookId = Book.objects.get(pk=request.data["book_id"])
      genreId = Genre.objects.get(pk=request.data["genre_id"])

      bookGenre = BookGenre.objects.create(
          book=bookId,
          genre=genreId,
      )
      serializer = BookGenreSerializer(bookGenre)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      bookId = Book.objects.get(pk=request.data["book"])
      genreId = Genre.objects.get(pk=request.data["genre"])
      
      bookGenre = BookGenre.objects.get(pk=pk)
      bookGenre.book_id = bookId
      bookGenre.genre_id = genreId

      bookGenre.save()

      serializer = BookGenreSerializer(bookGenre)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
      bookGenre = BookGenre.objects.get(pk=pk)
      bookGenre.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)


class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = ('id', 'book', 'genre' )
        depth = 1
