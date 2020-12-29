$('form').submit(function() {
  $(this).find("button[type='submit']").prop('disabled',true);
});

$('#showUpdatedNoModal').modal('show');

/*
$(document).ready(function () {
    $("#set_read").click(function () {
        $("#readstatus").fadeOut(function () {
            $("#readstatus").text(($("#readstatus").text() == 'Leido') ? 'No Leido' : 'Leido').fadeIn();
        })
    })
});


function change(button_id, a_id)
{
    //var xhr = new XMLHttpRequest();
    var elem = document.getElementById(button_id);
    if (elem.value=="Marcar como leido") {
        elem.value = "Marcar como no leido";
    }
    else elem.value = "Marcar como leido";
}*/


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
const csrftoken = getCookie('csrftoken');


$(document).ready(function() {
    $('.readstatus').on('click', 'button', function () {

        if($(this).attr('data-read')=="True"){
            $(this).text("marcar como leido")
            $(this).attr('data-read', "False")
        }
        else {
            $(this).text("marcar como no leido")
            $(this).attr('data-read', "True")
        }
        $.ajax('/toggle_read/' + $(this).data('article-id') + '/', {
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken
            }
        })
    })

});

/*



  invoke = (event) => {
    let nameOfFunction = this[event.target.name];
    let arg1 = event.target.getAttribute('data-arg1');
    if (elem.value=="Marcar como leido") {
        elem.value = "Marcar como no leido";
    }
    else elem.value = "Marcar como leido";
}
    // We can add more arguments as needed...
    window[nameOfFunction](arg1)
    // Hope the function is in the window.
    // Else the respective object need to be used
  }

   */