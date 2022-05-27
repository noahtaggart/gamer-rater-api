"""Module for generating bottom 5 games report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all


class MostReviewedGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                g.*,
                COUNT(r.id) as ReviewCount
                from raterapp_game g
                join raterapp_review r on r.game_id = g.id
                GROUP by g.id
                order by ReviewCount desc 
                limit 1
                """)
            
            most_reviewed_game = dict_fetch_all(db_cursor)
            
        template = 'games/most_reviewed_game.html'
            
        context = {
            "most_reviewed_game": most_reviewed_game
        }
        
        return render(request, template, context)
