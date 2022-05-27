"""Module for generating games with more than 5 players report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all


class MoreThan5PlayersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
                SELECT
                g.*
                from raterapp_game g
                Where g.number_of_players >= 5
                """)

            dataset = dict_fetch_all(db_cursor)

            more_than_5 = []

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
                more_than_5.append(game)

        template = 'games/list_more_than_5_players.html'

        context = {
                "more_than_5_players_list": more_than_5
            }

        return render(request, template, context)
