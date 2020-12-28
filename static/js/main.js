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

*/
function change(button_id, a_id)
{
    //var xhr = new XMLHttpRequest();
    var elem = document.getElementById(button_id);
    if (elem.value=="Marcar como leido") {
        elem.value = "Marcar como no leido";
    }
    else elem.value = "Marcar como leido";
}


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