from django.shortcuts import reverse,redirect
from .utils import *
from django.conf import settings
from django.http import JsonResponse
from mendeley import Mendeley
from mendeley.session import MendeleySession

def get_article_from_data(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            query = request.POST['query'].split(';')
            mendeley = Mendeley(settings.MENDELEY_ID, settings.MENDELEY_SECRET)
            auth = mendeley.start_client_credentials_flow().authenticate()


            for i in query:
                if query == '': continue
                get_data_by_query(auth.token['access_token'],query=i)

            if request.user.keywords:
                for i in request.user.keywords:
                    get_data_by_query(auth.token['access_token'],query=i)

            if request.user.authors:
                for i in request.user.authors:
                    get_article_from_authors(i,auth.token['access_token'])

            if request.user.tags:
                for i in request.user.tags:
                    get_data_by_query(auth.token['access_token'],query=i)

            return JsonResponse({"success":"Success"})
