from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    content = models.TextField(unique=True)
    
    def __str__(self):
        return self.content



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = "like_posts", blank=True)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    
    def __str__(self):
        return self.content
        
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to='posts/images',							# 저장 위치
        processors=[ResizeToFill(600, 600)],		# 처리할 작업 목록
        format='JPEG',													# 저장 포맷
        options={'quality': 90},								# 옵션
    )

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    def __str__(self):
        return self.content