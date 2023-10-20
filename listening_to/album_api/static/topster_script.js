



window.onload = function() {

    $(".album_container").sortable({
        connectWith: ".album_container"
    });
    $(".album_container").disableSelection();
    /*
    
    $('.album_container').each( function(){
        var this_element = "#" + this.id;
        console.log(this_element);
        $(this_element).sortable();
    });
    */
  
        
        

    /*Sortable.create(large, {
        animation: 100,
        group: "shared",
        easing: "cubic-bezier(1, 0, 0, 1)",
        sort: true
    })
    Sortable.create(med, {
        animation: 100,
        group: "shared",
        easing: "cubic-bezier(1, 0, 0, 1)",
        sort: true
    })
    Sortable.create(small, {
        animation: 100,
        group: "shared",
        easing: "cubic-bezier(1, 0, 0, 1)",
        sort: true
    })
    */
};
