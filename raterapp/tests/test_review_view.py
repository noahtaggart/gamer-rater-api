from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapp.models import Game, Player, Review
from raterapp.views.review import ReviewSerializer

class ReviewTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'players', 'games', 'reviews',]
    
    def setUp(self):
        # Grab the first Player object from the database and add their token to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_review(self):
        """create review test"""
        
        game = Game.objects.first()
        
        url = "/reviews"
        review = {
            "game": game.id,
            "content": "This is a review of a game",
            "player": self.player.id
        }
        
        response = self.client.post(url, review, format='json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_review = Review.objects.last()
        expected = ReviewSerializer(new_review)
        self.assertEqual(expected.data, response.data)