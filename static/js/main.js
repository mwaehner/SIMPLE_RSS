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



var toggleReadStatusOnButtonClick = {
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

var setReadStatusOnLinkClick = {
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

function showModalWithText(toShowModal, text){
    toShowModal.find('.modal-body').text(text);
    toShowModal.modal('show');
}

var addSubscriptionsToFolderOnClick = {
    init : function () {
        $('#add_to_folder_button').on('click', function () {
            var selected = [];
            $('#subscriptions input:checked').each(function() {
                selected.push($(this).data('subscription-id'));
            });
            var toShowModal = $('#genericModal')
            if(!selected.length){
                showModalWithText(toShowModal, "Please select at least one subscription")
                return;
            }
            var folder = $("#folder_selection option:selected")
            var folderId = folder.val();
            if(!folderId){
                showModalWithText(toShowModal, "Please select a folder")
                return;
            }
            $.ajax('/add_subscriptions_to_folder', {
                type: 'POST',
                data: {
                    folderId: folderId,
                    subscriptionIds: JSON.stringify(selected),
                    csrfmiddlewaretoken: csrftoken
                },
                success: function () {
                    $('#subscriptions input:checked').each(function() {
                        var folderName = folder.text()
                        selected.push($(this).data('subscription-id'));
                        var newFolderHtmlElement = $("<span class='folder-name' name=" + folderName + "></span>").text(folderName);
                        var folders = $(this).next(".folders")
                        var withThisname = folders.find("span[name='" + folderName + "']")
                        if(! withThisname.length){
                            folders.append(newFolderHtmlElement)
                        }
                    });
                    toShowModal = $('#successModal')
                    showModalWithText(toShowModal, "Subscriptions added to folder")

                },
                error: function (request, status, error) {
                    toShowModal = $('#failureModal')
                    showModalWithText(toShowModal, request.responseText)
                }
            })

    })
    }
}

var changeSelectedNumberOnCheck = {
    init : function () {
        $('#subscriptions :checkbox').change(function() {
            var selectedNumber = $('#selectedNumber');
            var checkedCheckboxesCount = $('input:checkbox:checked').length;
            selectedNumber.text(checkedCheckboxesCount)
        });
    }
}

var addNewFolderOnClick = {
    init : function () {
        $('#folder_form').on('submit', function() {
            event.preventDefault();
            var form = $(this)
            var optionsCount = $('#folder_selection').children('option').length;
            $.ajax(form.attr('action'),{
                type: 'POST',
                data: form.serialize(),
                success: function (result){
                    var toShowModal = $('#successModal')
                    showModalWithText(toShowModal, "Added new folder")
                    var newOption = $('<option></option>')
                    var folderName = form.serializeArray()[0]['value']
                    newOption.append(folderName)
                    CORREGIR ESTO: TIENE QUE DEVOLVER ID EN LA BD newOption.attr('value',optionsCount+1 )
                    newOption.attr('name',folderName )
                    $('#folder_selection').append(newOption)
                },
                error: function (result){
                    var toShowModal = $('#failureModal')
                    showModalWithText(toShowModal, "Folder already exists")
                },
                csrfmiddlewaretoken: csrftoken
            })

            $(this).find("button[type='submit']").removeProp('disabled')

        });
    }
}



$(document).ready( function() {
    $('form').submit(function() {
        $(this).find("button[type='submit']").prop('disabled',true);
    });
    toggleReadStatusOnButtonClick.init()
    setReadStatusOnLinkClick.init()
    addSubscriptionsToFolderOnClick.init()
    addNewFolderOnClick.init()
    changeSelectedNumberOnCheck.init()

    $('#showUpdatedCountModal').modal('show');

});
