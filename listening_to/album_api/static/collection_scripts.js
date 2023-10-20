function change_collections(albums,collection_slug){
    $.ajax({
        url: '/change_collection',
        data: {
            'albums' : JSON.stringify(albums),
            'collection_slug' : collection_slug
        },
        dataType : 'json',
        success: function(data){
            window.location.href = '/thanks-for-submitting';
        },
        error: function() {
            window.location.href = '/failed-submission';
        }
    });
}
//the following function is used for the user search page, the only such function on this file. Why is this here? no one knows
function get_users(search_substring){
    $.ajax({
        url: '/get_user_search',
        data: {
            'user_name_substring' : search_substring
        },
        dataType : 'json',
        success: function(data){
            $('.big_link').remove();
            for(let i = 0; i < data['users'].length; i++){
                boi = $('.user-search-results');
                user = data['users'][i]
                new_user = document.createElement('a');
                new_user.href = '/user/' + user['username'];
                new_user.className = 'big_link';
                new_user.style = "display: block;";
                new_user.innerHTML = user['username'];
                boi.append(new_user);
                
            }
            console.log(data['users']);
        },
        error: function() {
            console.log('failed submission!');
        }
    });
}

function resize_columns(){
    var width_height_ratio = $(window).width() / $(window).height();
    if( width_height_ratio >= 1.72){
        $('.album_list').css("grid-template-columns",'repeat(2, 0.5fr)');
    }
    else {
        $('.album_list').css("grid-template-columns",'repeat(1, 1fr)');
    }
}



$(document).ready(function(){
    resize_columns();
    $(".album_checkbox_selector").change(function(){
        if ($(".album_checkbox_selector").is(":checked")){
            $(".action_selection").attr("style","display: inline-block;");
            // iterate through, pass to ajax call on selected action. Selected action will be parametre to call. Return redirect.
            //console.log("Checked(at least 1 of em");
        }
        else{ 
            $(".action_selection").attr("style","display: none;");
        }
    });
    //Check if action selection is for collection change:
    $(".action_selection_box").change(function(){
        var selected_action = $('.action_selection_box').val();
        if(selected_action == 'move_collection'){
            $(".collection_selection_box").attr("style","display: inline-block;");
        }
        else{
            $(".collection_selection_box").attr("style","display: none;");
        }
    });
    
    $(".submit_button").click(function(){
        var selected_action = $('.action_selection_box').val();
        const selected_albums = [];
        var album_checkboxes = $(".album_checkbox_selector");

        if(selected_action != ""){
            for( var i = 0; i < album_checkboxes.length; i++){
                var selected_box = album_checkboxes[i]
                if(selected_box['checked'] == true){
                    selected_albums.push(selected_box['value']);
                }
            }
        }
        if(selected_action == "move_collection"){
            if(confirm("Are you sure you want to change these albums' collections?")){
                var new_collection = $('.collection_selection_box').val();
                change_collections(selected_albums,new_collection);
            }
        }
        else if(selected_action == "delete"){
            if(confirm("Are you sure you want to delete these albums?")){
                delete_albums(selected_albums);
            }
        }
        console.log(selected_albums);
    });


    $(".select_all_checkboxes").change(function(){
        
        if ($(".select_all_checkboxes").is(":checked")){
            $('input:checkbox').not(this).prop('checked', this.checked);
            $('input:checkbox').not(this).change();
        }
        else{ 
            $('input:checkbox').not(this).prop('checked', this.checked);
            $('input:checkbox').not(this).change();
        }
    });
});

$(window).on('resize', function() {
    resize_columns();
})
