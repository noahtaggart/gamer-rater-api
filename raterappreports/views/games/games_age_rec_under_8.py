"""Module for generating games with age rec less than 8 report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all


class GamesAgeRecUnder8List(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                select 
                *
                from raterapp_game g 
                where g.age_recommendation < 8
                """)
            
            dataset = dict_fetch_all(db_cursor)
            
            games_under_8 = []
            
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
                "creator_id": row['creator_id']
            }
                games_under_8.append(game)
                
        template = 'games/list_games_age_rec_under_8.html'
        
        context = {
            "games_age_rec_under_8": games_under_8
        }
        
        return render(request, template, context)