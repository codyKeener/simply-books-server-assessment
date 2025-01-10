from django.db import models
from django.core.validators import MinValueValidator
from .author import Author

class Book(models.Model):
  
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
  title = models.CharField(max_length=50)
  image = models.URLField()
  price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0.00)])
  sale = models.BooleanField()
  uid = models.CharField(max_length=30)
  description = models.CharField(max_length=280)
