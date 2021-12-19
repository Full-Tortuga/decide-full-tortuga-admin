export function getCookie(name:string) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function checkPasswordEqual(event:any){
    var pwd = event.target.password.value;
    var pwd2 = event.target.password2.value;
    var equal = pwd == pwd2;
    if(!equal){
        event.preventDefault();
    }

}