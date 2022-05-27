"""Module for generating games per category report"""
from re import template
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all

class GamesPerCategoryList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
                SELECT
                c.id,
    c.label,
    COUNT(gc.category_id) as GamesPerCategory

    from raterapp_game g
    join raterapp_game_category gc on g.id = gc.game_id
    join raterapp_category c on gc.category_id = c.id
    group by g.id
    order by GamesPerCategory DESC
    """)
            
            dataset = dict_fetch_all(db_cursor)
            
            games_per_category = []
            
            for row in dataset:
                count = {
                    "id": row['id'],
                    "label": row['label'],
                    "GamesPerCategory": row['GamesPerCategory']
                }
                games_per_category.append(count)
                
        template = 'games/list_games_per_category.html'
        
        context = {
            "games_per_category_list": games_per_category
        }
        
        return render(request, template, context)