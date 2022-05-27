from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapp.models import Game, Player, Rating
from raterapp.views.rating import RatingSerializer

class RatingTests(APITestCase):
    
    fixtures = ['users', 'tokens', 'players', 'games', 'ratings',]
    
    def setUp(self):
        # Grab the first Player object from the database and add their token to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_rating(self):
        """create rating test"""
        
        game = Game.objects.first()
        
        url = "/ratings"
        rating = {
            "game": game.id,
            "rating": 10
        }
        
        response = self.client.post(url, rating, format='json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_rating = Rating.objects.last()
        
        expected = RatingSerializer(new_rating)
        self.assertEqual(expected.data, response.data)
        
    def test_change_rating(self):
        """Change rating test"""
        rating = Rating.objects.first()
        
        url = f'/ratings/{rating.id}'
        
        updated_rating = {
            "game": rating.game.id,
            "rating": 1
        }
        
        response = self.client.put(url, updated_rating, format='json')
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        rating.refresh_from_db()
        
        self.assertEqual(updated_rating['rating'], rating.rating)