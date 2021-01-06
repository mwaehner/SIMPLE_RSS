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



var toggle_read_status_on_button_click = {
    init : function () {
        $('.readstatus').on('click', 'button', function () {
            var article = $(this).closest(".article")
        $.ajax('/toggle_read/' + article.data('article-id') + '/', {
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrftoken
            },
            success: function() {
                if(article.attr('data-read')=="True"){
                    article.attr('data-read', "False")
                }
                else {
                    article.attr('data-read', "True")
                }
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        })

    })
    }

}

var set_read_status_on_link_click = {
    init : function () {
        $('.article-text').on('click', 'a', function () {
            var article = $(this).closest(".article")
            $.ajax('/set_read/' + article.data('article-id') + '/', {
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: csrftoken
                },
                success: function () {
                    article.attr('data-read', "True")
                },
                error: function (request, status, error) {
                    alert(request.responseText);
                }
            })
    })
    }
}

var add_to_folder_on_click = {
    init : function () {
        $('#add_to_folder_button').on('click', function () {
            //alert("blabla")
            var selected = [];
            $('#subscriptions input:checked').each(function() {
                selected.push($(this).data('subscription-id'));
                //alert($(this).data('subscription-id'))
            });
            folderName = $("#folder_selection option:selected").text();
            //var article = $(this).closest(".article")
            $.ajax('/add_subscriptions_to_folder', {
                type: 'POST',
                data: {
                    folder: folderName,
                    subscriptions: JSON.stringify({ 'selectedSubscriptions': selected }),
                    csrfmiddlewaretoken: csrftoken
                },
                success: function () {
                    alert("Successfully added to folder")
                },
                error: function (request, status, error) {
                    alert(request.responseText);
                }
            })
    })
    }
}


$(document).ready( function() {
    toggle_read_status_on_button_click.init()
    set_read_status_on_link_click.init()
    add_to_folder_on_click.init()
    $('form').submit(function() {
        $(this).find("button[type='submit']").prop('disabled',true);
    });
    $('#showUpdatedNoModal').modal('show');

});
