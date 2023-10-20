function delete_object(object_type, object_slug){
    if(confirm("Are you sure you want to delete?")){
        $.ajax({
            url: '/delete_object',
            data: {
                'object_type' : object_type,
                'object_slug' : object_slug
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
}
function delete_albums(albums){
    $.ajax({
        url: '/delete_albums',
        data: {
            'albums' : JSON.stringify(albums)
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