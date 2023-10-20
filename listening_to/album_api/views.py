import re
#from django.conf.urls import url
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render#, render_to_response
from album_api.models import *
from django.forms.models import model_to_dict
from album_api.serializers import *
from album_api.forms import *
import urllib
import json
from operator import attrgetter
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

def return_sorted_albums(queryset_albums):
    return sorted(queryset_albums, key=attrgetter('alphabetical_title'), reverse=False)

def home_page(request):
    return render(request, 'home_page.html')


def user_page(request, user_name):
    _user = User.objects.get(username=user_name)
    #GETTING HOME PAGE
    if request.method == 'GET':
        #determining first name:
        display_name = user_name if _user.first_name == '' or None else _user.first_name
        #determining if is owner or not
        is_owner = True if request.user == _user else False

        lt_albums = return_sorted_albums(Album.objects.all().filter(listening_to=True,user=_user))#lt_albums = listening_to_albums

        serialized_lt_albums = AlbumSerializer(lt_albums, many=True)
        collection = Collection.objects.all().filter(user=_user)[0] #just grab most recent one
        serialized_collection = model_to_dict(collection)
        return render(request, 'user_page.html', {'display_name' : display_name,'is_owner' : is_owner, 'owner': user_name,'lt_albums' : serialized_lt_albums, 'collection' : serialized_collection, 'backlog_form' : BacklogAlbumSubmissionForm()})
    
    elif request.method == 'POST':
        #BACKLOG SUBMISSION
        form = BacklogAlbumSubmissionForm(request.POST)
        try:
            if form.is_valid():
                #yea this is lazy-- i should check if existing beforehand, but due to case n stuff, i cant
                backlog_collection = Collection.objects.all().filter(user=_user, title="The Backlog.")[0]
                backlog_album = Album(title=form.cleaned_data['album_title'],creator=form.cleaned_data['artist'],collection=backlog_collection)
                backlog_album.save()
                existing_albums = Album.objects.filter(title=backlog_album.title,user=_user,creator=backlog_album.creator).count()
                if existing_albums > 1:
                    backlog_album.delete()
            return HttpResponseRedirect('/thanks-for-submitting')
        except:
            return HttpResponseRedirect('/failed-submission')



def list_all_collections(request, user_name):
    _user =  User.objects.get(username=user_name)
    collections = Collection.objects.all().filter(user=_user)
    is_owner = True if request.user == _user else False
    #ughhhhh this inefficiency and overruse of data pains me but i am too lazy to fix lol
    serialized_collections = CollectionSerializer(collections,many=True)
    return render(request,'collection/list_collections_page.html',{'owner': user_name,'is_owner' : is_owner, 'collections' : serialized_collections.data})
    
def collection_page(request,user_name, title_slug):
    _user =  User.objects.get(username=user_name)
    is_owner = True if request.user == _user else False
    collection = Collection.objects.all().filter(user=_user,slug=title_slug)[0]
    serialized_collection = CollectionSerializer(collection)
    #Other collection options; for owner editing purposes.
    other_collections = Collection.objects.all().filter(user=_user).exclude(slug=title_slug)
    serialized_other_collections = CollectionSerializer(other_collections,many=True)
    return render(request, 'collection/view_collection_page.html', {'owner': user_name, 'is_owner' : is_owner, 'title' : serialized_collection.data['title'], 'albums' : serialized_collection.data['albums'], 'other_collections' : serialized_other_collections.data})

def list_all_albums(request, user_name):
    _user =  User.objects.get(username=user_name)
    is_owner = True if request.user == _user else False
    backlog_collection = Collection.objects.all().filter(user=_user, slug="the-backlog")[0]
    albums = return_sorted_albums(Album.objects.all().filter(user=_user).exclude(collection=backlog_collection))
    serialized_albums = AlbumSerializer(albums, many=True)
    other_collections = Collection.objects.all().filter(user=_user)
    serialized_other_collections = CollectionSerializer(other_collections,many=True)
    return render(request,'collection/view_collection_page.html',{'owner': user_name, 'is_owner' : is_owner, 'title' : 'All Albums', 'albums' : serialized_albums.data,'other_collections' : serialized_other_collections.data})

def album_review_page(request,user_name, album_slug):
    _user =  User.objects.get(username=user_name)
    _album = Album.objects.all().filter(user=_user,slug=album_slug)[0]
    serialized_album = AlbumSerializer(_album)
    return render(request,'album/album_review_page.html', {'owner': user_name,'album' : serialized_album.data})

def list_all_lists(request, user_name):
    _user =  User.objects.get(username=user_name)
    lists = List.objects.all().filter(user=_user)
    is_owner = True if request.user == _user else False
    serialized_lists = ListSerializer(lists, many=True)
    return render(request,'list/list_lists_page.html',{'owner': user_name,'is_owner' : is_owner, 'lists' : serialized_lists.data})

def temporary(request, user_name, list_slug):
    _user =  User.objects.get(username=user_name)
    _list= List.objects.all().filter(user=_user,slug=list_slug)[0]
    serialized_list = ListSerializer(_list)
    return render(request,'temporary.html',{'list' : serialized_list.data})

def list_page(request, user_name, list_slug):
    _user =  User.objects.get(username=user_name)
    _list= List.objects.all().filter(user=_user,slug=list_slug)[0]
    serialized_list = ListSerializer(_list)
    return render(request,"list/view_list_page.html", {'list' : serialized_list.data})

def list_form_page(request, list_slug=None):
    #user = request.user
    if request.method == 'GET':
        list_form = ListModelForm()

        object_formset = AlbumListObjectFormset(form_kwargs={'user' : request.user})
        if list_slug == None:
            #list creation
            return render(request,"list/list_form_page.html", {'list_form' : list_form, 'object_formset' : object_formset, 'list' : None})
        else:
            #list editing
            _list = List.objects.all().filter(user=request.user, slug=list_slug)[0]
            serialized_list = ListSerializer(_list)
            return render(request,"list/list_form_page.html", {'list_form' : list_form, 'object_formset' : object_formset, 'list' : serialized_list.data})

    elif request.method == 'POST':
        try:
            _list_form = ListModelForm(request.POST)
            
            _object_formset = AlbumListObjectFormset(data=request.POST,form_kwargs={'user' : request.user}) 
            if _list_form.is_valid() and _object_formset.is_valid():
                if List.objects.all().filter(user=request.user, slug=list_slug).count() >= 1:
                    #delete the old boi, in wit da new boi
                    if list_slug != None:
                        List.objects.all().filter(user=request.user, slug=list_slug)[0].delete()
                    else:
                        raise("List already exists!!!")
                new_list = List(
                    user = request.user,
                    title = _list_form.cleaned_data['title']
                )
                new_list.save()
                
                for album_object in _object_formset.cleaned_data:
                    if album_object != {}:
                        new_album_object = AlbumListObject(
                            _list = new_list,
                            album = Album.objects.all().filter(user=request.user,slug=album_object['album'])[0],
                            blurb=album_object['blurb']
                        )
                        new_album_object.save()
                return HttpResponseRedirect('/thanks-for-submitting')
            return HttpResponseRedirect('/failed-submission')
        except:
            return HttpResponseRedirect('/object-exists')


def album_form_page(request, album_slug=None):
    if request.method == 'GET':
        if album_slug == None:
            #album creation
            temp = AlbumForm(request.user)
            return render(request,'album/album_form_page.html', {'form' : temp, 'album' : None})
        else:
            #album editing
            _album = Album.objects.all().filter(user=request.user, slug=album_slug)[0]
            serialized_album = AlbumSerializer(_album)
            return render(request,'album/album_form_page.html', {'form' : AlbumForm(request.user, initial=serialized_album.data), 'album' : serialized_album.data})
    elif request.method == 'POST':
        #get the perps out

        form = AlbumForm(request.user,request.POST)
        try:
            if form.is_valid():

                new_album = Album(title=form.cleaned_data['title'],
                    creator=form.cleaned_data['creator'],
                    collection=form.cleaned_data['collection'],
                    listening_to=form.cleaned_data['listening_to'])
                if form.cleaned_data['score'] != None:
                    new_album.score = form.cleaned_data['score']
                if form.cleaned_data['review'] != '':
                    new_album.review = form.cleaned_data['review']
                if form.cleaned_data['album_art_url'] != None:
                    new_album.album_art_url = form.cleaned_data['album_art_url']
                
                #check if album exists already for user:
                possible_collections = Collection.objects.all().filter(user=request.user)
                if album_slug != None:
                        Album.objects.all().filter(collection__in=possible_collections, slug=album_slug)[0].delete()
                elif Album.objects.all().filter(collection__in=possible_collections, slug=slugify(new_album.title + new_album.creator)).count() >= 1:
                    raise('Already created')
                
                new_album.save()
                return HttpResponseRedirect('/thanks-for-submitting')
            else:
                return HttpResponseRedirect('/failed-form')
        #todo: fix exceptions for specific errors; currently catch-all for duplicate object creation. this applies to list_form and collection_form, too.
        except:
            return HttpResponseRedirect('/object-exists')

def collection_form_page(request, collection_slug=None):
    if request.method == 'GET':

        if collection_slug == None:
            #collection creation
            return render(request,'collection/collection_form_page.html', {'form' : CollectionForm(), 'collection' : None})
        else:
            #collection editing
            _collection = Collection.objects.all().filter(user=request.user, slug=collection_slug)[0]
            serialized_collection = CollectionSerializer(_collection)
            return render(request,'collection/collection_form_page.html', {'form' : CollectionForm(initial=serialized_collection.data), 'collection' : serialized_collection.data})
    
    elif request.method == 'POST':

        form = CollectionForm(request.POST)
        try:
            if form.is_valid():
                new_collection = Collection(title=form.cleaned_data['title'],
                    start_date = form.cleaned_data['start_date'],
                    user = request.user)
                new_collection.save()
                if Collection.objects.all().filter(slug=collection_slug,user=request.user).count() >= 1:
                    if collection_slug != None:
                        old_collection = Collection.objects.all().filter(slug=collection_slug,user=request.user)[0]
                        temp_query = old_collection.albums.all()
                        temp_query.update(collection=new_collection)
                        #old_collection.albums.all().update(collection=new_collection)
                        old_collection.delete()
                        new_collection.save()
                    else:
                        raise('Collection already exists!')
                new_collection.save()
                return HttpResponseRedirect('/thanks-for-submitting')
        except:
            return HttpResponseRedirect('/object-exists')










def create_form_page(request):
    return render(request,'create_form_page.html')

def user_search_page(request):
    return render(request,'user_search_page.html')

def thank_you_page(request):
    return render(request,'thank_you.html')

def about_page(request):
    return render(request,'about_page.html')

def support_page(request):
    return render(request, 'support_page.html')
def failed_submission_page(request):
    return render(request, "failed_submission.html")

def object_exists_page(request):
    return render(request, "object_exists.html")

def get_album_art(request):
    album_title = request.GET.get('album_title')
    creator = request.GET.get('creator')
    info = get_album_info(creator,album_title)
    text = info['album']['image'][4]['#text']
    return JsonResponse({'album_art_url' : text})

def get_albums_from_artist(request):
    artist = request.GET.get('artist')
    albums = Album.objects.all().filter(user=request.user,creator=artist)
    serialized_albums = AlbumSerializer(albums,many=True)
    return JsonResponse({'albums' : serialized_albums.data})

def get_user_search(request):
    user_name_substring = request.GET.get('user_name_substring')
    users = User.objects.all().filter(username__icontains=user_name_substring)
    serialized_users = UserSerializer(users,many=True)
    return JsonResponse({'users' : serialized_users.data})
        
def change_collection(request):
    album_slugs = json.loads(request.GET.get("albums"))
    collection_slug = request.GET.get('collection_slug')
    collection = Collection.objects.all().filter(user=request.user,slug=collection_slug)[0]
    for album_slug in album_slugs:
        album = Album.objects.all().filter(user=request.user,slug=album_slug)[0]
        album.collection = collection
        album.save()
    return JsonResponse({'resp' : 'success!'})

def delete_albums(request):
    album_slugs = json.loads(request.GET.get("albums"))
    for album_slug in album_slugs:
        album = Album.objects.all().filter(user=request.user,slug=album_slug)[0]
        album.delete()
    return JsonResponse({'resp' : 'success!'})

def delete_object(request):
    object_type = request.GET.get('object_type')
    object_slug = request.GET.get('object_slug')
    if object_type == 'album':
        Album.objects.all().filter(user=request.user,slug=object_slug)[0].delete()
    elif object_type == 'collection':
        Collection.objects.all().filter(user=request.user,slug=object_slug)[0].delete()
    elif object_type == 'list':
        List.objects.all().filter(user=request.user,slug=object_slug)[0].delete()
    return JsonResponse({'resp' : 'success!'})

import_albums = [
    ['The Impossible Kid', 'Aesop Rock'],
    ['1000 gecs','100 gecs'],
    ['syro','aphex twin'],
    ['selected ambient works 85-92','aphex twin'],
    ['amok','atoms for peace'],
    ['abbey road','the beatles'],
    ['magical mystery tour','the beatles'],
    ['revolver','the beatles'],
    ['sgt peppers lonely hearts club band','the beatles'],
    ['post','bjork'],
    ['debut','bjork'],
    ['vespertine','björk'],
    ['for the first time','black country, new road'],
    ['schlagenheim','black midi'],
    ['cavalcade','black midi'],
    ['bon iver','bon iver'],
    ['for emma, forever ago','bon iver'],
    ['visions of bodies being burned','clipping'],
    ['clppng','clipping'],
    ['czarface meets metalface','czarface'],
    ['super what?','czarface'],
    ['tron: legacy','daft punk'],
    ['alive 2007','daft punk'],
    ['david bowie','david bowie'],
    ['blackstar','david bowie'],
    ['aladdin sane','david bowie'],
    ['the rise and fall of ziggy stardust','david bowie'],
    ['hunky dory','david bowie'],
    ['no love deep web','death grips'],
    ['the money store','death grips'],
    ['ex military','death grips'],
    ['government plates','death grips'],
    ['year of the snitch','death grips'],
    ['bottomless pit','death grips'],
    ['the powers that b','death grips'],
    ['blonde','frank ocean'],
    ['demon days','gorillaz'],
    ['plastic beach','gorillaz'],
    ['death of an optimist','grandson'],
    ['injury reserve','injury reserve'],
    ['4:44','jay-z'],
    ['watch the throne','jay-z'],
    ['axis:bold as love','jimi hendrix'],
    ['electric ladyland','jimi hendrix'],
    ['are you experienced','jimi hendrix'],
    ['ballads 1','joji'],
    ['nectar','joji'],
    ['unknown pleasures','joy division'],
    ['jesus is king','kanye west'],
    ['my beautiful dark twisted fantasy','kanye west'],
    ['ye','kanye west'],
    ['808s and heartbreak','kanye west'],
    ['the college dropout','kanye west'],
    ['graduation','kanye west'],
    ['late registration','kanye west'],
    ['yeezus','kanye west'],
    ['the life of pablo','kanye west'],
    ['untitled unmastered','kendrick lamar'],
    ['section 80','kendrick lamar'],
    ['damn','kendrick lamar'],
    ['good kid, m.a.a.d city','kendrick lamar'],
    ['to pimp a butterfly','kendrick lamar'],
    ['man on the moon: the end of day','kid cudi'],
    ['man on the moon ii: the legend of mr. rager','kid cudi'],
    ['man on the moon iii: the chosen','kid cudi'],
    ["passion, pain and demon slayin'",'kid cudi'],
    ['kids see ghosts','kids see ghosts'],
    ['In the Court of the Crimson King','king crimson'],
    ['Once in a Long, Long While...','low roar'],
    ['0','low roar'],
    ['circles','mac miller'],
    ['madvillainy','mf doom'],
    ['mm food','mf doom'],
    ['oracular spectacular','mgmt'],
    ['thriller','michael jackson'],
    ['nehruviandoom','nehruviandoom'],
    ['harvest','neil young'],
    ['in the aeroplane over the sea','neutral milk hotel'],
    ['brick body kids still daydream','open mike eagle'],
    ['anime, trauma and divorce','open mike eagle'],
    ['hella personal film festival','open mike eagle'],
    ['stankonia','outkast'],
    #['fenghuang','pernelle'],
    ['punisher','phoebe bridgers'],
    ['mass teen fainting','plumtree'],
    ['predicts the future','plumtree'],
    ['daytona','pusha t'],
    ['amnesiac','radiohead'],
    ['a moon shaped pool','radiohead'],
    ['ok computer','radiohead'],
    ['the bends','radiohead'],
    ['the king of limbs','radiohead'],
    ['in rainbows','radiohead'],
    ['kid a','radiohead'],
    ['classics','ratatat'],
    ['californication','red hot chili peppers'],
    ['pony','rex orange county'],
    ['run the jewels 3','run the jewels'],
    ['run the jewels 4','run the jewels'],
    ['run the jewels 2','run the jewels'],
    ['run the jewels','run the jewels'],
    ['meat is murder','the smiths'],
    ['the queen is dead','the smiths'],
    ["tomorrow's modern boxes",'thom yorke'],
    ['the eraser','thom yorke'],
    ['it is what it is','thundercat'],
    ['drunk','thundercat'],
    ['flower boy','tyler the creator'],
    ['igor','tyler the creator'],
    ['weezer','weezer'],
    ['music from saharan cellphones','various artists'],
    ['pinkerton','weezer'],

]
#DEBUG IMPORT PAGE THINGY-- this is buggy and stupid as shit
def debug_import_page(request):
    _collection = Collection.objects.all().filter(title="Grade 11.")[0]
    joey_user = User.objects.get(username='joeymartin')
    for _album in import_albums:
        try:
            new_album = Album(title=_album[0],creator=_album[1],collection=_collection,user=request.user)
            new_album.save()
        except:
            print(_album[0])
        
    return render(request,'collection/list_collections_page.html')


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


