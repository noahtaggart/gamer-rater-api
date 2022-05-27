"""Module for generating bottom 5 games report"""
from re import template
from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all

class PlayerMostGames(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            db_cursor.execute("""
                SELECT *
                FROM (
                        SELECT
                            p.*,
                            u.first_name || " " || u.last_name AS full_name,
                            COUNT(g.creator_id) AS games_added
                        FROM raterapp_player p
                        LEFT JOIN raterapp_game g
                            ON p.id = g.creator_id
                        JOIN auth_user u
                            ON p.id = u.id
                        GROUP BY p.id
                )
                WHERE games_added = (
                    SELECT
                        MAX(games_added)
                    FROM (
                        SELECT
                            p.*,
                            COUNT(g.creator_id) AS games_added
                        FROM raterapp_player p
                        LEFT JOIN raterapp_game g
                            ON p.id = g.creator_id
                        GROUP BY p.id
                    )
                )""")
            
            dataset = dict_fetch_all(db_cursor)
            
            player_most_games = []
            
            for row in dataset:
                player = {
                    "id": row['id'],
                    "bio": row['bio'],
                    "user_id": row['user_id'],
                    "full_name": row['full_name'],
                    "games_added": row['games_added']
                }
                
                player_most_games.append(player)
                
        template = 'players/list_player_most_games.html'
        
        context = {
            "player_most_games": player_most_games
        }
        
        return render(request, template, context)