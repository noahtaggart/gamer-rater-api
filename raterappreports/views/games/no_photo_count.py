"""Module for generating games with more than 5 players report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all


class NoPhotoCount(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                COUNT(g.id) as NoPhotoCount
                from raterapp_game g 
                left join raterapp_photo p on p.game_id = g.id
                WHERE p.photo ISNULL """)
            
            dataset = dict_fetch_all(db_cursor)
            
            no_photo_count = []
            
            for row in dataset:
                count = {
                    "NoPhotoCount": row['NoPhotoCount']
                }
                no_photo_count.append(count)
                
        template = 'games/list_num_of_games_without_pics.html'
            
        context = {
            "no_photo_count": no_photo_count
        }
        
        return render(request, template, context)