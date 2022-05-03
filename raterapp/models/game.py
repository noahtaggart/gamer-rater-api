from django.db import models
from .rating import Rating


class Game(models.Model):
    title = models.CharField(max_length=50)
    designer = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    year_released = models.IntegerField()
    number_of_players = models.IntegerField()
    age_recommendation = models.IntegerField()
    creator = models.ForeignKey("Player", on_delete=models.CASCADE)
    estimated_time_to_play = models.CharField(max_length=50)
    category = models.ManyToManyField("Category", related_name="categories")
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = Rating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        if len(ratings) > 0:
            for rating in ratings:
                total_rating += rating.rating
            average_rating = total_rating / len(ratings)
            return average_rating
            

        # Calculate the averge and return it.
        # If you don't know how to calculate averge, Google it.
    
    
    
    
    