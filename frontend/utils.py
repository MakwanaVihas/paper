import django
from django.conf import settings

import requests
from api.models import Article,Authors
from django.db.models import ObjectDoesNotExist
import json

def get_data_by_query(token,query):
    from django.conf import settings
    import requests
    from api.models import Article,Authors
    from django.db.models import ObjectDoesNotExist
    import json

    import time
    time.sleep(0.1)

    ids = []
    headers = {"Authorization": 'Bearer '+token}
    linit=100
    try:
        response = requests.get(f'https://api.mendeley.com/search/catalog?query={query}&view=all&open_access=True&limit={linit}',headers=headers).json()
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        response = requests.get(f'https://api.mendeley.com/search/catalog?query={query}&view=all&open_access=True&limit={linit}',headers=headers).json()

    for i,res in enumerate(response):

        if 'identifiers' not in res:
            continue
        if 'authors' in res:
            authors = []
            for i in res['authors']:
                f_name = None if 'first_name' not in i or i['first_name']=='' else i['first_name']
                l_name = None if 'last_name' not in i or i['last_name']=='' else i['last_name']
                if f_name or l_name:
                    first = f_name if f_name else ''
                    last = l_name if l_name else ''

                    author,cr = Authors.objects.get_or_create(name = first+" "+last,done=False)
                else:
                    author,cr = Authors.objects.get_or_create(name = 'Anonymous',done=False)

                author.save()
                authors.append(author)

        else:
            authors = []
            author,cr = Authors.objects.get_or_create(name = 'Anonymous',done=False)

            author.save()
            authors.append(author)

        try:
            article = Article.objects.get(id=res['id'])

        except ObjectDoesNotExist:
            article = Article(
                title = res['title'],type = res['type'],id=res['id'],
                year = res['year'] if 'year' in res else 2000,
                source = res['source'] if 'source' in res else "Not specified",
                publisher = res['publisher'] if 'publisher' in res else 'Anonymous',
                identifiers=res['identifiers'],
                link = res['link'],
                pdf = res['pdf'] if 'pdf' in res else None,
                keywords = res["keywords"][:6] if "keywords" in res else None,
                reader_count = res['reader_count'] if 'reader_count' in res else 0,
                reader_count_by_academic_status = res['reader_count_by_academic_status'] if 'reader_count_by_academic_status' in res else '{}',
                reader_count_by_subject_area = res['reader_count_by_subject_area'] if 'reader_count_by_subject_area' in res else '{}',
                reader_count_by_country = res['reader_count_by_country'] if 'reader_count_by_country' in res else '{}',
            )
            article.save()

            for i in authors:
                article.authors.add(i)

        ids.append(article.pk)
    return ids

def get_data(token):
    from django.conf import settings
    import requests
    from api.models import Article,Authors
    from django.db.models import ObjectDoesNotExist
    import json

    import time
    time.sleep(0.1)



    headers = {"Authorization": 'Bearer '+token}
    for key,val in settings.SUBDISCIPLINES.items():
        for sub in val:
            linit = 10
            query = sub.replace(" ","+").lower()
            print(query)
            try:
                response = requests.get(f'https://api.mendeley.com/search/catalog?query={query}&view=all&open_access=True&limit={linit}',headers=headers).json()
            except requests.exceptions.ConnectionError:
                print("okay_bitxh")
                time.sleep(5)
                response = requests.get(f'https://api.mendeley.com/search/catalog?query={query}&view=all&open_access=True&limit={linit}',headers=headers).json()

            for i,res in enumerate(response):
                print(i)
                if 'identifiers' not in res:
                    continue
                if 'authors' in res:
                    authors = []
                    for i in res['authors']:
                        f_name = None if 'first_name' not in i or i['first_name']=='' else i['first_name']
                        l_name = None if 'last_name' not in i or i['last_name']=='' else i['last_name']
                        if f_name or l_name:
                            first = f_name if f_name else ''
                            last = l_name if l_name else ''

                            author,cr = Authors.objects.get_or_create(name = first+" "+last,done=False)
                        else:
                            author,cr = Authors.objects.get_or_create(name = 'Anonymous',done=False)

                        author.save()
                        authors.append(author)

                else:
                    authors = []
                    author,cr = Authors.objects.get_or_create(name = 'Anonymous',done=False)

                    author.save()
                    authors.append(author)


                article = Article(
                    title = res['title'],type = res['type'],id=res['id'],
                    year = res['year'] if 'year' in res else 2000,
                    source = res['source'] if 'source' in res else "Not specified",
                    publisher = res['publisher'] if 'publisher' in res else 'Anonymous',
                    identifiers=res['identifiers'],
                    link = res['link'],
                    pdf = res['pdf'] if 'pdf' in res else None,
                    keywords = res["keywords"][:6] if "keywords" in res else None,
                    reader_count = res['reader_count'] if 'reader_count' in res else 0,
                    reader_count_by_academic_status = res['reader_count_by_academic_status'] if 'reader_count_by_academic_status' in res else '{}',
                    reader_count_by_subject_area = res['reader_count_by_subject_area'] if 'reader_count_by_subject_area' in res else '{}',
                    reader_count_by_country = res['reader_count_by_country'] if 'reader_count_by_country' in res else '{}',
                )
                article.save()

                for i in authors:
                    article.authors.add(i)


def get_article_from_authors(author_name,token):

    if author_name == "Anonymous":
        return

    from django.conf import settings
    import django

    import requests
    from django.core.exceptions import ObjectDoesNotExist
    from api.models import Article,Authors
    from django.db.models import ObjectDoesNotExist
    import json
    import time
    if Authors.objects.get(name=author_name).done:
        return


    headers = {"Authorization": 'Bearer '+token}
    try:
        response = requests.get(f'https://api.mendeley.com/search/catalog?author={author_name}&view=all&open_access=True&limit=100',headers=headers).json()

    except requests.exceptions.ConnectionError:
        print("okay_bitxh")
        time.sleep(5)
        response = requests.get(f'https://api.mendeley.com/search/catalog?author={author_name}&view=all&open_access=True&limit=100',headers=headers).json()

    for i,res in enumerate(response):
        print(i)
        if 'identifiers' not in res:
            continue

        if 'authors' in res:
            authors = []
            for i in res['authors']:
                f_name = None if 'first_name' not in i or i['first_name']=='' else i['first_name']
                l_name = None if 'last_name' not in i or i['last_name']=='' else i['last_name']
                if f_name or l_name:
                    first = f_name if f_name else ''
                    last = l_name if l_name else ''

                    try:
                        author = Authors.objects.get(name = first+" "+last)
                    except ObjectDoesNotExist:
                        author = Authors(name = first+" "+last,done = False)

                else:
                    try:
                        author = Authors.objects.get(name = 'Anonymous')
                    except ObjectDoesNotExist:
                        author = Authors(name = 'Anonymous',done = False)

                author.save()
                authors.append(author)

        else:
            authors = []
            author,cr = Authors.objects.get_or_create(name = 'Anonymous')

            author.save()
            authors.append(author)

        try:
            Article.objects.get(id=res['id'])

        except ObjectDoesNotExist:

            article = Article(
                title = res['title'],type = res['type'],id=res['id'],
                year = res['year'] if 'year' in res else 2000,
                source = res['source'] if 'source' in res else "Not specified",
                publisher = res['publisher'] if 'publisher' in res else 'Anonymous',
                identifiers=res['identifiers'],
                link = res['link'],
                pdf = res['pdf'] if 'pdf' in res else None,
                keywords = res["keywords"][:6] if "keywords" in res else None,
                reader_count = res['reader_count'] if 'reader_count' in res else 0,
                reader_count_by_academic_status = res['reader_count_by_academic_status'] if 'reader_count_by_academic_status' in res else '{}',
                reader_count_by_subject_area = res['reader_count_by_subject_area'] if 'reader_count_by_subject_area' in res else '{}',
                reader_count_by_country = res['reader_count_by_country'] if 'reader_count_by_country' in res else '{}',
            )
            try:
                article.save()
                for i in authors:
                    article.authors.add(i)
            except django.db.utils.DataError:
                pass
