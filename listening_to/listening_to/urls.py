"""listening_to URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from album_api.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path(r'user/<str:user_name>', user_page),

    path(r'user/<str:user_name>/collection', list_all_collections), #list all collections
    path(r'user/<str:user_name>/collection/<slug:title_slug>', collection_page), #look at collection

    path(r'user/<str:user_name>/album', list_all_albums), #list all albums
    path(r'user/<str:user_name>/album/<slug:album_slug>', album_review_page), #look at album
    
    path(r'user/<str:user_name>/list', list_all_lists),
    path(r'user/<str:user_name>/list/<slug:list_slug>', list_page),

    path('form', create_form_page),

    path(r'form/album', album_form_page), #add album
    path(r'form/album/<slug:album_slug>', album_form_page), #edit album

    path(r'form/collection',collection_form_page), #add collection
    path(r'form/collection/<slug:collection_slug>',collection_form_page), #edit collection
    
    path(r'form/list', list_form_page), #add album
    path(r'form/list/<slug:list_slug>', list_form_page), #edit album
    
    path('thanks-for-submitting', thank_you_page),
    path('support-the-creator', support_page),
    path('about-page', about_page),
    path('failed-submission', failed_submission_page),
    path('object-exists',object_exists_page),
    path('search', user_search_page),
    path('get_album_art',get_album_art),
    path('get_albums_from_artist',get_albums_from_artist),
    path('change_collection',change_collection),
    path('get_user_search', get_user_search),
    path('delete_object', delete_object),
    #TODO: MAKE THE FOLLOWING URL/VIEW REDUNDANTTTTT
    path('delete_albums', delete_albums),


    path(r'user/temp/<str:user_name>/list/<slug:list_slug>', temporary),
    path('accounts/signup', SignUpView.as_view(),name='sign_up'), # new

    path('accounts/', include('django.contrib.auth.urls')),
]
