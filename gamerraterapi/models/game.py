from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=55)
    description = models.CharField(max_length=200)
    designer = models.CharField(max_length=50)
    year_released = models.IntegerField()
    num_of_players = models.IntegerField()
    time_to_play = models.IntegerField()
    age_rec = models.IntegerField()
    categories = models.ManyToManyField("Category", through="GameCategory", related_name="categories")