function get_albums(artist,element,album_val){
    $.ajax({
        url: '/get_albums_from_artist',
        data: {
            'artist' : artist,
        },
        dataType : 'json',
        success: function(data){
            var albums = data['albums'];
            var space = element.find(".album_field");
            space.attr("style", "display: inline-block");
            if (space.parent().find(".album_field_label").length == false){
                //if no label is there, create one(must be manually made due to formset limitation)
                space.before(`<label class="album_field_label" for=".album_field">Enter Album:</option>`)
            }
            space.find('option').remove();
            for(let i = 0; i < albums.length; i++){
                var album = albums[i];
                space.append(`<option value="${album.slug}">${album.title}</option>`);
            }
            if(album_val != null){
                space.val(album_val);
            }
        },
        error: function() {
            console.log('failed submission!');
        }
    });
}
function load_album_choices(artist_field,artist_val=null){
    var artist = artist_field.parent().find(".artist_field option:selected").text();
    get_albums(artist,artist_field.parent().parent(),artist_val);
}
function load_form(artist,album,blurb){
    let birdForm = document.querySelectorAll(".list_object_form")
    let container = document.querySelector("#form-container")
    let addButton = document.querySelector("#add-form")
    let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
    let newForm = birdForm[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d){1}-`,'g')
    let formNum = birdForm.length-1
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)

    //KEEP DIFFERENCE BETWEEN NULL AND '' NOTED FOR FUTURE JOEY!!!!!!!!
    if (album == ''){
        $(newForm).children().find(".album_field").val(null);
        $(newForm).children().find(".album_field").attr("style", "display: none");
        $(newForm).children().find(".album_field_label").remove();
    }
    if (artist != ''){
        $(newForm).children().find(".artist_field").val(artist);
        load_album_choices($(newForm).children().find(".artist_field"),album);

    }
    if (blurb != ''){
        var text = blurb.replaceAll('<br>','\n');
        $(newForm).children().find(".blurb_field").val(text);
    }
    $(newForm).append(`<button class="delete_button" id="delete_form" type="button">Delete album from list.</button>`);
    container.insertBefore(newForm, addButton);
    
    totalForms.setAttribute('value', `${formNum+1}`)
    
}
function delete_form(element){
    //element is form container, fyi.
    element.remove();
}
$(document).ready(function(){
    $("#form-container").sortable({
        items: ".list_object_form"
    });
    $("#form-container").submit(function(e){
        $(this).children('.list_object_form').each(function () {
            var album_val = $(this).children().find('.album_field').val();
            console.log(album_val);
            if (album_val == "" || album_val == null){
                alert('Remove any empty albums from the list creation.');
                e.preventDefault();
            }
            
        });
        
    });
});
