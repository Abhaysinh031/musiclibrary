from django.db import models
from django.contrib.auth.models import User

class Music(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    file = models.FileField(upload_to='music/')
    

    def __str__(self):
        return self.title

class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ManyToManyField(Music, blank=True, related_name='folders')
    is_favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # music = models.ManyToManyField(Music)
    music = models.ManyToManyField(Music, related_name='favorite_music')
    folders = models.ManyToManyField(Folder, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Favorites"
