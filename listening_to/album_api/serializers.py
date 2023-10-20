from rest_framework import serializers
from album_api.models import *
from django.contrib.auth.models import User
from operator import attrgetter

def return_sorted_albums(queryset_albums):
    return sorted(queryset_albums, key=attrgetter('alphabetical_title'), reverse=False)

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'




class CollectionSerializer(serializers.ModelSerializer):
    albums = serializers.SerializerMethodField()
    class Meta:
        model = Collection
        fields = '__all__'
    
    def get_albums(self,instance):
        albums = return_sorted_albums(instance.albums.all())
        return AlbumSerializer(albums, many=True).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AlbumListObjectSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    class Meta:
        model = AlbumListObject
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    album_objects = AlbumListObjectSerializer(many=True)
    class Meta:
        model = List
        fields = '__all__'