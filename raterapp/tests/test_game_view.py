from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapp.models import Game, Player
from raterapp.views.game import GameSerializer

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'players', 'games', 'categories', 'game_category']
    
    def setUp(self):
        # Grab the first Player object from the database and add their token to the headers
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Clue",
            "designer": "Milton Bradley",
            "description": "Board game",
            "year_released": 2016,
            "number_of_players": 6,
            "age_recommendation": 1,
            "estimated_time_to_play": "2 days",
            "creator": self.player.id,
            "category": [1]
        }
        
        

        response = self.client.post(url, game, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        # Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = GameSerializer(new_game)

        # Now we can test that the expected ouput matches what was actually returned
        self.assertEqual(expected.data, response.data)
        
    def test_get_game(self):
        """Get Game Test
        """
        # Grab a game object from the database
        game = Game.objects.first()

        url = f'/games/{game.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the game through the serializer that's being used in view
        expected = GameSerializer(game)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)
        
    def test_list_games(self):
        """Test list games"""
        url = '/games'

        response = self.client.get(url)
        
        # Get all the games in the database and serialize them to get the expected output
        all_games = Game.objects.all()
        expected = GameSerializer(all_games, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertEqual(expected.data, response.data)
        
    def test_change_game(self):
        """Change game test"""
        # Grab the first game in the database
        game = Game.objects.first()
        
        url = f'/games/{game.id}'

        # Define the Game properties
        # The keys should match what the change method is expecting
        # Make sure this matches the code you have
        updated_game = {
            "title": f'{game.title} updated',
            "designer": game.designer,
            "description": game.description,
            "year_released": game.year_released,
            "number_of_players": game.number_of_players,
            "age_recommendation": game.age_recommendation,
            "estimated_time_to_play": game.estimated_time_to_play
        }
        
        

        response = self.client.put(url, updated_game, format='json')

        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        # Get the last game added to the database, it should be the one just created
        game.refresh_from_db()

        # assert that the updated value matches
        self.assertEqual(updated_game['title'], game.title)
        
    def test_delete_game(self):
        """Test delete game"""
        game = Game.objects.first()

        url = f'/games/{game.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the game
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)