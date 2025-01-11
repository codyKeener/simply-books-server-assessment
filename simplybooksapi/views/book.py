from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Book, Author

class BookView(ViewSet):
  
  def retrieve(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    
    try:
    # IF THERE IS NOT A UID, GET THE BOOK THAT MATCHES THE PK (PUBLIC BOOKS)
      if uid is None:
        book = Book.objects.get(pk=pk)
    # IF THERE IS A UID, GET THE BOOK THAT MATCHES THE PK AND THE UID (PRIVATE BOOKS)
      else:
        book = Book.objects.get(pk=pk, uid=uid)
      
      serializer = BookSerializer(book)
      return Response(serializer.data)
    
    except Book.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)    
    
  def list(self, request):
    
    # GET THE AUTHOR FROM THE REQUEST PARAMETERS
    author = request.query_params.get('author', None)
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    # GET THE SALE VALUE FROM THE REQUEST PARAMETERS
    sale = request.query_params.get('sale', None)
    
    # IF TRUE IS PASSED IN THE FAVORITE PARAMETER INSTEAD OF 1, CONVERT TO 1
    if sale == True or sale == 'TRUE' or sale == 'true':
      sale = 1
    
    # IF FALSE IS PASSED IN THE FAVORITE PARAMETER INSTEAD OF 0, CONVERT TO 0
    if sale == False or sale == 'FALSE' or sale == 'false':
      sale = 0
    
    try: 
      books = Book.objects.all()
      
      # FILTER BOOKS BY UID IF UID IS PASSED IN THE QUERY PARAMETERS (PRIVATE BOOKS)
      if uid is not None:
        books = books.filter(uid=uid)
      
      # FILTER BOOKS BY AUTHOR IF AUTHOR IS PASSED IN THE QUERY PARAMETERS (WORKS FOR PUBLIC OR PRIVATE BOOKS)
      if author is not None:
        books = books.filter(author=author)
      
      # FILTER BOOKS BY SALE IF SALE IS PASSED IN THE QUERY PARAMETERS (WORKS FOR PUBLIC OR PRIVATE BOOKS)  
      if sale is not None:
        books = books.filter(sale=sale)
        
      serializer = BookSerializer(books, many=True)
      return Response(serializer.data)
    except:
      return Response({'message': 'Check query'}, status=status.HTTP_400_BAD_REQUEST)
  
  def create(self, request):
    
    author = Author.objects.get(pk=request.data["author_id"])
    
    try:
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
    except:
      # IF ALL VALUES ARE NOT PRESENT IN THE REQUEST, THE BOOK WILL NOT BE CREATED
      return Response({'message': 'All data points must be provided: author_id, title, image, price, sale, uid, description'}, status=status.HTTP_417_EXPECTATION_FAILED)
  
  def update(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    author = Author.objects.get(pk=request.data["author_id"])
    
    id = pk
    book = Book.objects.get(pk=pk)
    
    # IF A UID IS NOT PASSED IN THE QUERY PARAMETERS, RETURN AN ERROR BECAUSE WE NEED TO VERIFY THAT THE USER REQUESTING TO UPDATE THE BOOK IS THE USER THAT CREATED THE BOOK (PRIVATE BOOKS)
    if uid == None:
      return Response({'message': 'Must provide the uid of the user requesting to update the book in the query parameters'}, status=status.HTTP_403_FORBIDDEN)
    # IF THE UID PASSED IN THE QUERY PARAMETERS IS THE SAME AS THE UID OF THE BOOK, UPDATE THE BOOK (PRIVATE BOOKS)
    elif book.uid == uid:
      try:
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
      except:
        # IF ALL VALUES ARE NOT PRESENT IN THE REQUEST, THE BOOK WILL NOT BE UPDATED
        return Response({'message': 'All data points must be provided: author_id, title, image, price, sale, uid, description'}, status=status.HTTP_417_EXPECTATION_FAILED)
      
  def destroy(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    book = Book.objects.get(pk=pk)
    
    if uid == None:
      return Response({'message': 'Must provide the uid of the user requesting to delete the book in the query parameters'}, status=status.HTTP_403_FORBIDDEN)
    # IF THE UID PASSED IN THE QUERY PARAMETERS IS THE SAME AS THE UID OF THE BOOK, DELETE THE BOOK (PRIVATE BOOKS)
    elif book.uid == uid:
      try:
        book.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      except:
        return Response({'message': 'Check query'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      # IF THE UID IN THE QUERY PARAMETERS DOES NOT MATCH THE UID OF THE BOOK, RETURN AN ERROR BECAUSE THE USER THAT IS REQUESTING TO DELETE THE BOOK MUST BE THE USER THAT CREATED THE BOOK (PRIVATE BOOKS)
      return Response({'message': 'Only the user that created the author can delete it'}, status=status.HTTP_403_FORBIDDEN)
  
class BookSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Book
    fields = ('id', 'author', 'title', 'image', 'price', 'sale', 'uid', 'description')
    depth = 1
