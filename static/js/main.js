$('form').submit(function() {
  $(this).find("button[type='submit']").prop('disabled',true);
});

$('#showUpdatedNoModal').modal('show');
