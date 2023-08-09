from django.db import models
from django.contrib.auth.models import  AbstractUser, User
import datetime

# class UserManage(AbstractUser):
#     staff = models.BooleanField('is staff', default = False)

class Tags(models.Model):
   tag = models.CharField(max_length=50)

   def __str__(self):
        return self.tag

class Category(models.Model):
    name = models.CharField(max_length=39)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 255)
    brief_description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete =models.CASCADE)
    slug = models.CharField(max_length=130)
    timestamp = models.DateTimeField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , null=True, blank=True)
    thumbnail = models.ImageField('thumbnails')
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title +' '+ 'by' + '   @'+self.author.username



class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=39)
    # email = models.EmailField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=69, null=True)
    message = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)# subcomments
    timestamp = models.DateTimeField(default=datetime.datetime.now())
    # comment = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)# subcomment
    
class FeaturedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.post.sno) + self.post.title

class RecentWork(models.Model):
    img = models.ImageField(upload_to='recent_work')
    text = models.TextField()

    