
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






$(document).ready(function(){
    $('.username_entry').change(function(){
        var substring = $(".username_entry").val();
        get_users(substring);
    });
    get_users('');
});