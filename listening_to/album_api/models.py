from django.db import models
from django.db.models.fields import SlugField, related
from django.db.models.signals import post_save, post_init
import requests
from django.utils.text import slugify
from urllib.request import urlopen
from django.contrib.auth.models import User
from django.dispatch import receiver
import urllib
from django.db.models import F
import json
from django.db.models.functions import Lower

# Create your models here.

API_KEY = '2b04d59d250ef13a028401fbd3990ab3'

MANUAL_OVERRIDE = False




class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

def fix_space_bois(text):
    temp2 = text.encode(encoding= "UTF-8")
    temp = text.replace("&", "%26")
    return temp.replace(" ", "+")


def get_album_info(artist,album):
    url = 'https://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=' + API_KEY + '&artist=' + fix_space_bois(artist) + '&album=' + fix_space_bois(album) + '&format=json&autocorrect=1'
    album_json = requests.get(url).json()
    return album_json

class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='')
    start_date = models.DateField(blank=True,null=True)
    slug = models.SlugField(blank=True,default='')

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Collection, self).save(*args,**kwargs)

class Album(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    collection = models.ForeignKey(Collection, default='', related_name='albums', on_delete=models.CASCADE)

    title = models.CharField(default='',max_length=255)
    #sorting_title = models.CharField(default='',blank=True,max_length=255)

    creator = models.CharField(default='',blank=True,max_length=255)
    #sorting_creator = models.CharField(default='',blank=True,max_length=255)

    album_art_url = models.CharField(default='',max_length=255,blank=True)
    listening_to = models.BooleanField(default=False)
    review = models.TextField(blank=True,null=True, default=None)
    score = IntegerRangeField(default=None, null=True, blank=True, min_value=0, max_value=10)
    slug = SlugField(blank=True,default='')
    manual_override = models.BooleanField(default=False)

    @property
    def alphabetical_title(self):
        """
        Returns an alphabetical-friendly string of a title attribute.
        """
        title = self.creator.lower()

        # A list of flags to check each `title` against.
        starts_with_flags = [
            'the ',
            'an ',
            'a '
        ]

        # Check each flag to see if the title starts with one of it's contents.
        for flag in starts_with_flags:
            if title.lower().startswith(flag):
                # If the title does indeed start with a flag, return the title with
                # the flag appended to the end preceded by a comma.
                return "%s, %s" % (title[len(flag):], title[:len(flag)-1])
            else:
                pass
        # If the property did not return as a result of the previous for loop then just
        # return the title.
        return self.creator.lower()

    class Meta:
        ordering = ['creator','title']

    def __init__(self, *args, **kwargs):
        super(Album, self).__init__(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        #instance_info = self.cleaned_data
        self.user = self.collection.user
        self.slug = slugify(self.title + self.creator)
        #self.sorting_creator = return_sorting_text(self.creator)
        #self.sorting_title = return_sorting_text(self.title)
        try:
            if self.manual_override is False:
                #try:
                album_info = get_album_info(self.creator,self.title)
                #TODO: ADD THE FOLLOWING FOR BACKLOG SUBMISSIONS
                #if album_info['album']['image'][1]['#text'] == '':
                #    raise ValueError('album is empty')
                self.creator = album_info['album']['artist']
                self.title = album_info['album']['name']
                if self.album_art_url == '':
                    self.album_art_url = album_info['album']['image'][4]['#text']
                #except:
                    #print('welp, that failed. lol')
        except:
            pass
        super(Album, self).save(*args, **kwargs)



class List(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default='')
    slug = models.SlugField(blank=True,default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(List,self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class AlbumListObject(models.Model):
    _list = models.ForeignKey(List,default='', related_name="album_objects", on_delete=models.CASCADE)
    album = related.OneToOneField(Album,related_name="album", on_delete=models.CASCADE)
    blurb = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.blurb = self.blurb.replace('\r\n', '<br>')
        super(AlbumListObject,self).save(*args, **kwargs)
    
@receiver(post_save,sender=User)
def add_backlog(sender,instance, **kwargs):
    if kwargs.pop('created'):
        the_backlog = Collection(user=instance,title="The Backlog.",start_date='2004-12-06')
        the_backlog.save()