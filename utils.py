import django
from django.conf import settings

import requests
from api.models import Article,Authors
from django.db.models import ObjectDoesNotExist
import json
from frontend.utils import get_data


def authors_(token):
    from api.models import Article,Authors
    from frontend.utils import get_article_from_authors

    for j,i in enumerate(list(Authors.objects.all())):
        print("TURN: ",j)
        get_article_from_authors(i.name,token)
        i.done = True
        i.save()

from mendeley import Mendeley
from mendeley.session import MendeleySession

mendeley = Mendeley(8184, 'quTDlCgvGK9K3UvV')
auth = mendeley.start_client_credentials_flow().authenticate()
get_data(auth.token['access_token'])
