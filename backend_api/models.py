from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class Book(models.Model):
     name = models.CharField(max_length=200)
     author = models.CharField(max_length=200)
     year = models.IntegerField()
     isbn = models.CharField(max_length=20)
     quantity = models.IntegerField()
     tags = models.CharField(max_length=200)
     image = models.ImageField(default='default.jpg', upload_to='user_image')


class User(AbstractUser):
     username = models.CharField(max_length=100)
     email = models.EmailField(unique=True)
     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['username']

     def profile(self):
          profile = Profile.objects.get(user=self)


class Favourite(models.Model):
     user = models.ForeignKey(User, related_name="favourites", on_delete=models.CASCADE)
     book = models.ForeignKey(Book, related_name="favourited_by", on_delete=models.CASCADE)

     class Meta:
          unique_together = ("user", 'book')

     def __str__(self):
          return f'{self.book.name}-{self.user.username}'


class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     full_name = models.CharField(max_length=200)
     bio = models.CharField(max_length=300)
     image = models.ImageField(default='default.jpg', upload_to='user_image')
     verified = models.BooleanField(default=False)


class Rating(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     rating = models.IntegerField()

     class Meta:
          unique_together = ('user', 'book')

     def __str__(self):
          return f'{self.user} rated {self.book} with rating {self.rating}'



def create_user_profile(sender, instance, created, **kwargs):
     if created:
          Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

