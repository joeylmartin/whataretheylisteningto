import enum
from django import forms
from album_api.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.forms import BaseFormSet
# paste this at the start of code
import ssl 

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context




class BacklogAlbumSubmissionForm(forms.Form):
    album_title = forms.CharField(label='Enter Album Title',max_length=60)
    artist = forms.CharField(label='Enter Artist Name', max_length=25)

class AlbumForm(forms.Form):
    def __init__(self,_user, *args,**kwargs):
        super(AlbumForm,self).__init__(*args,**kwargs)
        self.fields['collection'].queryset = Collection.objects.all().filter(user=_user)

    collection= forms.ModelChoiceField(label='Series:', queryset=Collection.objects.all(),widget=forms.Select(attrs={'class' : 'collection_field'}))
    title = forms.CharField(label='Album Title:',max_length=70, widget=forms.TextInput(attrs={'class' : 'album_title_field'}))
    creator = forms.CharField(label='Artist Name:', max_length=70, widget=forms.TextInput(attrs={'class' : 'artist_field'}))
    listening_to = forms.BooleanField(label='Are you listening to it right now?',required=False)
    album_art_url = forms.CharField(label='Image URL:',required=False, max_length=1000, widget=forms.TextInput(attrs={'class' : 'album_art_url', 'hidden' : True}))
    review = forms.CharField(label='Review:', required=False,widget=forms.Textarea(attrs={'class': 'review_field'}))
    score = forms.IntegerField(label='Score:',required=False, min_value=0,max_value=10,widget=forms.NumberInput(attrs={'class' : 'score_field'}))

class CollectionForm(forms.Form):
    title = forms.CharField(label='Title:',widget=forms.TextInput(attrs={'class' : 'title_field'}))
    start_date = forms.DateField(label='Start Date of Series:',widget=forms.DateInput(attrs={'type' : 'date', 'class' : 'date_field'}))

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False,label="First Name:", help_text="Keep this field blank if you want your name anonymous.")
    class Meta:
        model = User
        fields = ("first_name","username")


class ListModelForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('title',)
        labels = {
            'title' : 'List Title:'
        }
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'list_title'})
        }

class AlbumListObjectForm(forms.Form):
    artist = forms.ChoiceField(required=True,label="Enter Artist",widget=forms.Select(attrs={'class' : 'artist_field'}))
    album = forms.CharField(required=True,label="",widget=forms.Select(attrs={'class' : 'album_field', 'style' : "display: none;"}))
    blurb = forms.CharField(label='Enter Blurb:',required=False,widget=forms.Textarea(attrs={'class' : "blurb_field"}))
    def __init__(self, *args,**kwargs):
        self.user = kwargs.pop('user', None)
        super(AlbumListObjectForm,self).__init__(*args,**kwargs)
        temp = list(dict.fromkeys(Album.objects.filter(collection__user=self.user).values_list('creator',flat=True)))
        self.fields['artist'].choices = zip(temp,temp)
        #correct ordering (in case of moving formsets) by appending order #
        self.data._mutable = True
        ordering_index = 0
        for key in self.data.keys():
            if 'ORDER' in key:
                self.data[key] = str(ordering_index)
                print(self.data[key])
                ordering_index += 1

        #
    #    if isinstance(user_name,str):

AlbumListObjectFormset = formset_factory(AlbumListObjectForm, can_order=True)