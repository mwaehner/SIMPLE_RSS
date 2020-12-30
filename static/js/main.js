$('form').submit(function() {
  $(this).find("button[type='submit']").prop('disabled',true);
});

$('#showUpdatedNoModal').modal('show');



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
    // toggling read status of article when clicking button
    $('.readstatus').on('click', 'button', function () {

        if($(this).attr('data-read')=="True"){
            $(this).text("marcar como leido")
            $(this).attr('data-read', "False")
            $(this).closest(".article").removeClass('read-article')
        }
        else {
            $(this).text("marcar como no leido")
            $(this).attr('data-read', "True")
            $(this).closest(".article").addClass('read-article')
        }

        $.ajax('/toggle_read/' + $(this).data('article-id') + '/', {
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken
            }
        })

    })

    //setting article as read when clicking on link
    $('.article-text').on('click', 'a', function () {

        var button = $(this).closest('.article-text').find('.toggle-unread')
        button.text("marcar como no leido")
        button.attr('data-read', "True")
        $(this).closest(".article").addClass('read-article')
        $.ajax('/set_read/' + button.data('article-id') + '/', {
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken
            }
        })
    })

});
