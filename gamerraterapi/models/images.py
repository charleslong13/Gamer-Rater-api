from django.db import models

class Image(models.Model):
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    imageURL = models.CharField(max_length=400)