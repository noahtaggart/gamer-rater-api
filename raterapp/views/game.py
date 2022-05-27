"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapp.models import Game, Player, Category
from rest_framework.decorators import action
from django.db.models import Q

class GameView(ViewSet):
    """"Rater app game view"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single game
        
        Returns:
            Response -- JSON serialized game
        """
        
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all games
        
        Returns:
            Response -- JSON serialized list of games
        """
        search_text = self.request.query_params.get('q', None)
        order_by = self.request.query_params.get('orderby', None)
        
        if order_by == None and search_text == None:
            games = Game.objects.all()    
        elif order_by == "year":
            games = Game.objects.order_by('-year_released')   
        elif order_by == "timeestimate":
            games = Game.objects.order_by('-estimated_time_to_play')   
        elif order_by == "designer":
            games = Game.objects.order_by('-designer')   
        else: 
            games = Game.objects.filter(
                Q(title__contains=search_text) |
                Q(description__contains=search_text) |
                Q(designer__contains=search_text)
)
        
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized game instance
        """
        
        creator = Player.objects.get(user=request.auth.user)
        # category = Category.objects.get(pk=request.data['category_id'])
        
        game = Game.objects.create(
            title=request.data['title'],
            designer=request.data['designer'],
            description=request.data['description'],
            year_released=request.data['year_released'],
            number_of_players=request.data['number_of_players'],
            age_recommendation=request.data['age_recommendation'],
            estimated_time_to_play=request.data['estimated_time_to_play'],
            creator = creator
    
        )
        game.category.add(*request.data['category'])
            
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    @action(methods=['post'], detail=True)
    def add_category(self, request, pk):
        """Post request for a user to sign up for an event"""
   
        game = Game.objects.get(pk=pk)
        category = Category.objects.get(pk=request.data['category_id'])
        game.category.add(category)
        return Response({'message': 'category added'}, status=status.HTTP_201_CREATED)   
    
    def update(self, request, pk):
        """Handle PUT requests for a game
        
        Returns:
        Response -- Empty body with 204 status code
        """
        
        game = Game.objects.get(pk=pk)
        game.title = request.data['title']
        game.designer = request.data['designer']
        game.description = request.data['description']
        game.year_released = request.data['year_released']
        game.number_of_players = request.data['number_of_players']
        game.age_recommendation = request.data['age_recommendation']
        game.estimated_time_to_play = request.data['estimated_time_to_play']
        
        game.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    
    class Meta:
        model = Game
        fields = ('id', 'title', 'designer', 'description', 'year_released', 'number_of_players', 'age_recommendation', 'estimated_time_to_play', "creator", "category", "average_rating" )
        depth = 1