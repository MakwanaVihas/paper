from django.urls import path
from . import views,get_articles


urlpatterns = [
    path('', views.ListArticles.as_view(),name='home'),
    path('get_article_data/',views.get_article_data,name='get_article_data'),
    path('library/',views.LibaraySet.as_view(),name='library'),
    path('library/<pk>/',views.LibraryDetail.as_view(),name='library_detail'),

    path('topics/',views.topics,name='topics'),
    path('add_remove_topic/',views.add_remove_topic,name="add_remove_topic"),
    path('add_or_remove_kw/',views.add_or_remove_kw,name='add_or_remove_kw'),
    path('add_or_remove_author/',views.add_or_remove_author,name='add_or_remove_author'),
    path('author/<pk>/',views.GetAuthor.as_view(),name="get_author"),
    path('load_articles_author/',views.load_articles_author,name='load_articles_author'),
    path('search/',views.search,name='search'),
    path('add_to_library/',views.add_to_library,name='add_to_library'),
    path('delete_library/',views.delete_library,name='delete_library'),

    path('article_api/<str:pk>/',views.DetailArticleAPI.as_view(),name='article_api'),
    path('article/<str:pk>/',views.DetailArticle.as_view(),name='article'),
    path('get_readers/<str:id>/',views.get_readers,name="get_readers"),
    path('update_review/',views.update_review,name='update_review'),
    path('get_recommendation/',views.get_recommendation,name='get_recommendation'),

    path('get_articles/get_article_from_data/',get_articles.get_article_from_data,name='get_article_from_data')
]
