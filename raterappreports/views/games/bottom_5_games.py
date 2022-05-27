"""Module for generating bottom 5 games report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all

class Bottom5GameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
                SELECT
            g.*,
            AVG(r.rating) as AverageRating

            from raterapp_game g
            join raterapp_rating r On r.game_id = g.id
            Group By g.id
            ORDER by "averagerating" asc
            Limit 5
            """)
            
            dataset = dict_fetch_all(db_cursor)
            
            bottom_5_games = []
            
            for row in dataset:
                game = {
                    "id": row['id'],
                    "title": row['title'],
                    "description": row['description'],
                    "designer": row['designer'],
                    "year_released": row['year_released'],
                    "estimated_time_to_play": row['estimated_time_to_play'],
                    "number_of_players": row['number_of_players'],
                    "age_recommendation": row['age_recommendation'],
                    "creator_id": row['creator_id'],
                    "AverageRating": row['AverageRating'],
                }
                bottom_5_games.append(game)
        
        # The template string must match the file name of the html template
        template = 'games/list_bottom_5_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "bottom5games_list": bottom_5_games
        }

        return render(request, template, context)