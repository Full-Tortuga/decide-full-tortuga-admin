//ajax function to send graphs to backend
$(document).ready(async function(){
    await new Promise(r => setTimeout(r, 1500));
    var canvas_elements=document.getElementsByClassName("chartjs-render-monitor")
    if (canvas_elements.length==2) {
        $('#bar-chart').addClass(function(){
            const csrf_cookie=getCookie('csrftoken');
            $.ajax({
                url: "graphs/",
                type: "POST",
                dataType:"json",
                data:{
                    type:$('#vot_type').val(),
                    graphs:graphs_images(),
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