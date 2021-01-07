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
            var selected = [];
            $('#subscriptions input:checked').each(function() {
                selected.push($(this).data('subscription-id'));
            });
            to_show_modal = $('#genericModal')
            if(!selected.length){
                to_show_modal.find('.modal-body').text("Please select at least one subscription");
                to_show_modal.modal('show');
                return;
            }
            var folderName = $("#folder_selection option:selected").text();
            if(folderName==="-"){
                to_show_modal.find('.modal-body').text("Please select a folder");
                to_show_modal.modal('show');
                return;
            }
            $.ajax('/add_subscriptions_to_folder', {
                type: 'POST',
                data: {
                    folder: folderName,
                    subscriptions: JSON.stringify({ 'selectedSubscriptions': selected }),
                    csrfmiddlewaretoken: csrftoken
                },
                success: function () {
                    $('#subscriptions input:checked').each(function() {
                        selected.push($(this).data('subscription-id'));
                        var new_folder_html_elem = $("<span class='folder-name' name=" + folderName + "></span>").text(folderName);
                        var folders = $(this).next(".folders")
                        var withThisname = folders.find("span[name='" + folderName + "']")
                        if(! withThisname.length){
                            folders.append(new_folder_html_elem)
                        }
                    });
                    to_show_modal.find('.modal-body').text("Success: subscriptions added to folder")
                    to_show_modal.modal('show');

                },
                error: function (request, status, error) {
                    to_show_modal.find('.modal-body').text(request.responseText)
                    to_show_modal.modal('show');
                }
            })
    })
    }
}

var change_selected_number_on_check = {
    init : function () {
        $('#subscriptions :checkbox').change(function() {
            var selectedNumber = $('#selectedNumber');
            var selectedNumberAsInt = parseInt(selectedNumber.text());
            if (this.checked) {
                selectedNumber.text(selectedNumberAsInt+1)
            } else {
                selectedNumber.text(selectedNumberAsInt-1)
            }
        });
    }
}

var add_new_folder_on_click = {
    init : function () {
        to_show_modal = $('#genericModal')
        modal_body = to_show_modal.find('.modal-body')
        $('#folder_form').on('submit', function() {
            event.preventDefault();
            var form = $(this)
            $.ajax(form.attr('action'),{
                type: 'POST',
                data: form.serialize(),
                success: function (result){
                    modal_body.text("Success: added new folder")
                    var newOption = $('<option></option>')
                    var folderName = form.serializeArray()[0]['value']
                    newOption.append(folderName)
                    newOption.attr('name',folderName )
                    $('#folder_selection').append(newOption)
                },
                error: function (result){
                    modal_body.text("Failure: folder already exists")
                },
                csrfmiddlewaretoken: csrftoken
            })
            to_show_modal.modal('show');
            $(this).find("button[type='submit']").removeProp('disabled')

        });
    }
}



$(document).ready( function() {
    $('form').submit(function() {
        $(this).find("button[type='submit']").prop('disabled',true);
    });
    toggle_read_status_on_button_click.init()
    set_read_status_on_link_click.init()
    add_to_folder_on_click.init()
    add_new_folder_on_click.init()
    change_selected_number_on_check.init()

    $('#showUpdatedNoModal').modal('show');

});
