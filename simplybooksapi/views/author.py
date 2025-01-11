from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Author, Book

class AuthorView(ViewSet):
  
  def retrieve(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    try:
      # IF THERE IS NOT A UID, GET THE AUTHOR THAT MATCHES THE PK (PUBLIC AUTHORS)
      if uid is None:
        author = Author.objects.get(pk=pk)
      # IF THERE IS A UID, GET THE AUTHOR THAT MATCHES THE PK AND THE UID (PRIVATE AUTHORS)
      else:
        author = Author.objects.get(pk=pk, uid=uid)
        
      book_count = Book.objects.filter(author=author).count()
      author.book_count = book_count
      serializer = SingleAuthorSerializer(author)
      return Response(serializer.data)
  
    except Author.DoesNotExist as ex:
      return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    # GET THE FAVORITE VALUE FROM THE REQUEST PARAMETERS
    favorite = request.query_params.get('favorite', None)
    
    # IF TRUE IS PASSED IN THE FAVORITE PARAMETER INSTEAD OF 1, CONVERT TO 1
    if favorite == True or favorite == 'TRUE' or favorite == 'true':
      favorite = 1
      
    # IF FALSE IS PASSED IN THE FAVORITE PARAMETER INSTEAD OF 0, CONVERT TO 0
    if favorite == False or favorite == 'FALSE' or favorite == 'false':
      favorite = 0
      
    try:
      authors = Author.objects.all()
      
      # FILTER AUTHORS BY UID IF UID IS PASSED IN THE QUERY PARAMETERS (PRIVATE AUTHORS). IF NO UID IS PASSED IN THE QUERY PARAMETERS, AUTHORS WILL NOT BE FILTERED (PUBLIC AUTHORS)
      if uid is not None:
        authors = authors.filter(uid=uid)
        
      # FILTER AUTHORS BY FAVORITE IF FAVORITE IS PASSED IN THE QUERY PARAMETERS
      if favorite is not None:
        # IF THERE IS ONLY A FAVORITE VALUE AND NO UID, THIS WILL RETURN AN ERROR BECAUSE FAVORITE AUTHORS CAN ONLY BE QUERIED FOR SPECIFIC USERS
        if uid is not None:
          authors = authors.filter(favorite=favorite)
        else:
          return Response({'message': 'Favorite authors can only be queried for specific users'}, status=status.HTTP_403_FORBIDDEN)
      
      serializer = AuthorSerializer(authors, many=True)
      return Response(serializer.data)
    except:
      return Response({'message': 'Check query'}, status=status.HTTP_400_BAD_REQUEST)
  
  def create(self, request):
    
    try:
      author = Author.objects.create(
        email=request.data["email"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        image=request.data["image"],
        favorite=request.data["favorite"],
        uid=request.data["uid"]
      )
      serializer = AuthorSerializer(author)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
      # IF ALL VALUES ARE NOT PRESENT IN THE REQUEST, THE AUTHOR WILL NOT BE CREATED
      return Response({'message': 'All data points must be provided: email, first_name, last_name, image, favorite, uid'}, status=status.HTTP_417_EXPECTATION_FAILED)
  
  def update(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    id = pk
    author = Author.objects.get(pk=pk)
    
    # IF A UID IS NOT PASSED IN THE QUERY PARAMETERS, RETURN AN ERROR BECAUSE WE NEED TO VERIFY THAT THE USER REQUESTING TO UPDATE THE AUTHOR IS THE USER THAT CREATED THE AUTHOR (PRIVATE AUTHORS)
    if uid == None:
      return Response({'message': 'Must provide the uid of the user requesting to update the author in the query parameters'}, status=status.HTTP_403_FORBIDDEN)
    # IF THE UID PASSED IN THE QUERY PARAMETERS IS THE SAME AS THE UID OF THE AUTHOR, UPDATE THE AUTHOR (PRIVATE AUTHORS)
    elif author.uid == uid:
      try:
        author.email=request.data["email"]
        author.first_name = request.data["first_name"]
        author.last_name = request.data["last_name"]
        author.image = request.data["image"]
        author.favorite = request.data["favorite"]
        author.uid = uid
        
        author.save()
        
        serializer = AuthorSerializer(author)    
        return Response(serializer.data, status=status.HTTP_200_OK)
      except:
        # IF ALL VALUES ARE NOT PRESENT IN THE REQUEST, THE AUTHOR WILL NOT BE UPDATED
        return Response({'message': 'All data points must be provided: email, first_name, last_name, image, favorite, uid'}, status=status.HTTP_417_EXPECTATION_FAILED)
    else:
      # IF THE UID IN THE QUERY PARAMETERS DOES NOT MATCH THE UID OF THE AUTHOR, RETURN AN ERROR BECAUSE THE USER THAT IS REQUESTING TO UPDATE THE AUTHOR MUST BE THE USER THAT CREATED THE AUTHOR (PRIVATE AUTHORS)
      return Response({'message': 'Only the user that created the author can update it'}, status=status.HTTP_403_FORBIDDEN)
  
  def destroy(self, request, pk):
    
    # GET THE UID FROM THE REQUEST PARAMETERS
    uid = request.query_params.get('uid', None)
    
    author = Author.objects.get(pk=pk)
    
    if uid == None:
      return Response({'message': 'Must provide the uid of the user requesting to delete the author in the query parameters'}, status=status.HTTP_403_FORBIDDEN)
    # IF THE UID PASSED IN THE QUERY PARAMETERS IS THE SAME AS THE UID OF THE AUTHOR, DELETE THE AUTHOR (PRIVATE AUTHORS)
    elif author.uid == uid:
      try:
        author.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      except:
        return Response({'message': 'Check query'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      # IF THE UID IN THE QUERY PARAMETERS DOES NOT MATCH THE UID OF THE AUTHOR, RETURN AN ERROR BECAUSE THE USER THAT IS REQUESTING TO DELETE THE AUTHOR MUST BE THE USER THAT CREATED THE AUTHOR (PRIVATE AUTHORS)
      return Response({'message': 'Only the user that created the author can delete it'}, status=status.HTTP_403_FORBIDDEN)
  
class AuthorSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Author
    fields = ('id', 'email', 'first_name', 'last_name', 'image', 'favorite', 'uid')
    
class SingleAuthorSerializer(serializers.ModelSerializer):
  
  book_count = serializers.IntegerField(default=None)
  
  class Meta:
    model = Author
    fields = ('id', 'email', 'first_name', 'last_name', 'image', 'favorite', 'uid', 'book_count', 'books')
    depth = 1
