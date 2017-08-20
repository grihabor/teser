
$(function () {
    $('#add_repository').submit(function () {
        console.log('Add repo');
        $.get("/add_repository", {
            url: $('#url').val(),
            branch: $('#branch').val()
        }, function (response) {
            console.log(response);
        });
    });
});
