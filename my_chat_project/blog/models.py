from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse
CustomUser = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
# Create your models here.


    def __str__(self):
        return self.title
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(CustomUser, username=username)
            return Post.objects.filter(author=user).order_by('-date_posted')
        else:
            return Post.objects.all().order_by('-date_posted')
      