
from django.urls import path

from .views import Top5GameList, Bottom5GameList, GamesPerCategoryList, MoreThan5PlayersList, MostReviewedGameList, PlayerMostGames, GamesAgeRecUnder8List, NoPhotoCount, PlayersMostReviews
from .views.base import BaseList

urlpatterns = [
    path('reports/top5games', Top5GameList.as_view()),
    path('reports/bottom5games', Bottom5GameList.as_view()),
    path('reports/categoryGameCounts', GamesPerCategoryList.as_view()),
    path('reports/morethan5', MoreThan5PlayersList.as_view()),
    path('reports/mostreviewedgame', MostReviewedGameList.as_view()),
    path('reports/playermostgames', PlayerMostGames.as_view()),
    path('reports/gamesunder8', GamesAgeRecUnder8List.as_view()),
    path('reports/gamesNoPics', NoPhotoCount.as_view()),
    path("reports/playersmostreviews", PlayersMostReviews.as_view()),
    path('reports/base', BaseList.as_view()),
]