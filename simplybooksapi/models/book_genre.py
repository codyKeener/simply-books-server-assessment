from django.db import models
from .book import Book
from .genre import Genre

class BookGenre(models.Model):

  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="genrebooks")
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="bookgenres")
