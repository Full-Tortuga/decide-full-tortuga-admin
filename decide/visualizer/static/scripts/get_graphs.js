//ajax function to send graphs to backend
$(document).ready(function(){
    if (document.body.contains(document.getElementsByTagName("canvas")[0])) {
        $('canvas:nth-of-type(2)').addClass(function(){
            const csrf_cookie=getCookie('csrftoken');
            $.ajax({
                url: "graphs/",
                type: "POST",
                data:{
                    graphs:graphs_images()
                },
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_cookie)
                },
                failure: function(data){
                    console.log(error)
                }     
            });
        });
    }
});

//retrieve canvas graphs as base64 encoded image
function graphs_images(){
    var graphs=document.getElementsByClassName("chartjs-render-monitor");
    var images=[];
    for (var i=0; i< graphs.length; i++){
        images.push(graphs[i].toDataURL());
    }
    return images
}

//function to retrieve csrf_cookie, copied from Django Docs
function getCookie(name) {  
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
