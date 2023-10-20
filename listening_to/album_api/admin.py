from django.contrib import admin
from album_api.models import *
from django import forms



admin.site.site_header = "what the fuck is oatmeal"




class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = []


class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    list_display = ('title','creator','collection')
    list_filter = ('creator','collection')


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ['slug']

class CollectionAdmin(admin.ModelAdmin):
    form = CollectionForm

admin.site.register(AlbumListObject)
admin.site.register(List)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Collection, CollectionAdmin)