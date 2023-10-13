from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publ_date = models.DateField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} by {self.author.username}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_of_the_comment = models.CharField(max_length=255)
    content_of_the_comment = models.TextField()
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author_of_the_comment}, {self.content_of_the_comment}, {self.date_of_creation}'

