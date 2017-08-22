
function add_repository(url) {

}

function show_deploy_key() {

}

$(function () {
    var state = 0,
        deploy_key = $("#deploy_key"),
        deploy_key_container,
        url = $("#url");

    deploy_key_container = deploy_key.parent();

    deploy_key.attr('readonly', 'readonly');
    deploy_key_container.hide();

    $('#add_repository').submit(function (e) {
        e.preventDefault();

        if (state === 0) {

            $.getJSON("/generate_deploy_key", {}, function (response) {
                console.log('Show key');
                console.log(response);
                deploy_key_container.show();
                deploy_key.val(response.deploy_key);
            });

        } else if (state === 1) {

            $.getJSON("/add_repository", {
                url: url.val(),
                deploy_key: deploy_key.val()
            }, function (response) {
                console.log('Add repo');
                console.log(response);
                url.val("");
                deploy_key_container.hide();
            });
        }
        state = 1 - state;

        return false;
    });
});
