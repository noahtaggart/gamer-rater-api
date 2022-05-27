"""Module for generating top 3 players by review count report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all


class PlayersMostReviews(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                p.*,
                u.first_name || " " || u.last_name AS full_name,
                COUNT(r.id) as ReviewCount
                from raterapp_player p
                join raterapp_review r on r.player_id = p.id
                JOIN auth_user u ON p.id = u.id
                GROUP by p.id
                order by ReviewCount desc 
                limit 3
                """)
            
            dataset = dict_fetch_all(db_cursor)
            
            players_most_reviewed = []
            
            for row in dataset:
                player = {
                    "id": row['id'],
                    'bio': row['bio'],
                    'user_id': row['user_id'],
                    'full_name': row['full_name'],
                    'ReviewCount': row['ReviewCount']
                }
                
                players_most_reviewed.append(player)
                
        template = 'players/list_players_with_most_reviews.html'
        
        context = {
            "players_most_reviews": players_most_reviewed
        }
        
        return render(request, template, context)