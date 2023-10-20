from django import template

register = template.Library()

@register.simple_tag
def return_album_text(album_title, creator):
    return album_title + ' by ' + creator

@register.simple_tag
def return_album_score(score_int):
    return str(score_int) + '/10'

@register.simple_tag
def return_collection_slug(page_username,collection_slug):
    return '/user/' + page_username + '/collection/' + collection_slug



@register.simple_tag
def return_album_edit_link(album_slug):
    if album_slug != '':
        return '/form/album/' + album_slug
    else:
        return '/form/album'
@register.simple_tag
def return_collection_edit_link(collection_slug):
    if collection_slug != '':
        return '/form/collection/' + collection_slug
    else:
        return '/form/collection'

@register.simple_tag
def return_list_edit_link(list_slug):
    if list_slug != '':
        return '/form/list/' + list_slug
    else:
        return '/form/list'
@register.simple_tag
def return_add_link():
    return '/form'


@register.simple_tag
def return_user_page_link(user_name):
    return '/user/' + user_name

@register.simple_tag
def return_review_link(page_username,album_review_slug):
    return '/user/' + page_username + '/album/' + album_review_slug

@register.simple_tag
def return_all_lists_link(page_username):
    return '/user/' + page_username + '/list'

@register.simple_tag
def return_all_albums_link(page_username):
    return '/user/' + page_username + '/album'

@register.simple_tag
def return_all_collections_link(page_username):
    return '/user/' + page_username + '/collection'

@register.simple_tag
def return_backlog_link(page_username):
    return '/user/' + page_username + '/collection/the-backlog'

@register.simple_tag
def return_list_link(page_username,list_slug):
    return '/user/' + page_username + '/list/' + list_slug

@register.filter(name='times') 
def times(number):
    return range(number)
