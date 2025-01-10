from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Book, Author

class BookView(ViewSet):
  
  def retrieve(self, request, pk):
    
    try:
      book = Book.objects.get(pk=pk)
      serializer = BookSerializer(book)
      return Response(serializer.data)
    except Book.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    
    uid = request.query_params.get('uid', None)
    author = request.query_params.get('author', None)
    
    if author is not None and uid is not None:
      books = Book.objects.all()
      books = books.filter(uid=uid, author=author)
    elif uid is not None:
      books = Book.objects.all()
      books = books.filter(uid=uid)
    elif author is not None:
      books = Book.objects.all()
      books = books.filter(author=author)
    elif author is None and uid is None:
      books = Book.objects.all()
        
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    
    author = Author.objects.get(pk=request.data["author_id"])
    
    book = Book.objects.create(
      author=author,
      title=request.data["title"],
      image=request.data["image"],
      price=request.data["price"],
      sale=request.data["sale"],
      uid=request.data["uid"],
      description=request.data["description"]
    )
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    
    author = Author.objects.get(pk=request.data["author_id"])
    
    id = pk
    book = Book.objects.get(pk=pk)
    book.author=author
    book.title = request.data["title"]
    book.image = request.data["image"]
    book.price = request.data["price"]
    book.sale = request.data["sale"]
    book.uid = request.data["uid"]
    book.description=request.data["description"]
    
    book.save()
    
    serializer = BookSerializer(book)    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    
    book = Book.objects.get(pk=pk)
    book.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
  
class BookSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Book
    fields = ('id', 'author', 'title', 'image', 'price', 'sale', 'uid', 'description')
    depth = 1
