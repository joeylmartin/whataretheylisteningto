
function checkURL(url) {
    return(url.match(/\.(jpeg|jpg|gif|png)$/) != null);
}
function reveal_url_field(){
    $(".album_art_url").removeAttr("hidden");
    $("#album_art_url_label").removeAttr("hidden");
    $("#album_art_url_label").css({"display":"inline-block"});
}
//function fillForms(album){
function fill_album_forms(collection,album_title,artist,listening_to,album_art_url,review,score){
    $(".collection_field").val(collection);
    $(".album_title_field").val(album_title);
    $(".artist_field").val(artist);
    //ugh i hate this syntax lol change later
    if(listening_to == 'True'){
        $("#id_listening_to").attr("checked",true);
    }
    else {
        $("#id_listening_to").attr("checked",false);
    }
    $(".album_art_url").val(album_art_url);
    reveal_url_field();
    if(review != 'None'){
        $(".review_field").val(review);
    }
    $(".score_field").val(score);
}
function fill_collection_forms(collection_title,collection_date){
    $(".title_field").val(collection_title);
    $(".date_field").val(collection_date);
}

function get_album_art(album_title, creator){
    $.ajax({
        url: '/get_album_art',
        data: {
            'album_title' : album_title,
            'creator' : creator 
        },
        dataType : 'json',
        success: function(data){
            if(data['album_art_url'] != ''){
                $(".album_art").attr("src",data['album_art_url']);
                $(".album_art_url").val(data['album_art_url']);
            }
            else{
                $(".album_art").attr("src","https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/1200px-Icon-round-Question_mark.svg.png");
                $(".album_art_url").val("");
            }
        },
        error: function() {
            $(".album_art").attr("src","https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/1200px-Icon-round-Question_mark.svg.png");
            $(".album_art_url").val("");
        }
    });
}
$(document).ready(function(){
    $(".album_form").submit(function(e){
        console.log("doing submit!!!");
        //var _url = data['image_url'];
        //var temp = $(this);
        var _url = $(".album_art_url").val();
        //var _url = $(this).parent().find(".album_art").attr("src");
        //console.log(_url);
        //var _url = $(this).parent.find("album_art").attr("src");
        //var _url = $(this).parent.find(".image_url").val();
        if(_url == ""){
            reveal_url_field();
            e.preventDefault();
            alert('Could not find album. Check for spelling errors, otherwise manually enter in the URL for the cover art.');
        }
        //TODO: ADD SUPPORT FOR BLOCKING FORM SUBMIT IF ALBUM EXISTS ALREADY
        else if(checkURL(_url) == false){
            alert('Error: URL does not lead to image.');
            e.preventDefault();
        }
        else {
            //$(".album_art").attr("src",_url);
            $(".album_form").submit();
        }
    });

    $('.album_title_field').change(function(){
        var parent_form = $(".album_form")
        var _title = parent_form.find(".album_title_field").val();
        var _creator = parent_form.find(".artist_field").val();
        get_album_art(_title,_creator);
    });
    $('.artist_field').change(function(){
        var parent_form = $(".album_form")
        var _title = parent_form.find(".album_title_field").val();
        var _creator = parent_form.find(".artist_field").val();
        get_album_art(_title,_creator);
    });
});