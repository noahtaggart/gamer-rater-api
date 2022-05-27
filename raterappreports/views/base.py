from django.shortcuts import render
from django.db import connection
from django.views import View

from raterappreports.views.helpers import dict_fetch_all

class BaseList(View):
    def get(self, request):
        
        # The template string must match the file name of the html template
        template = 'base.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "bottom5games_list": ""
        }

        return render(request, template, context)