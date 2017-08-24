
var failed_to_clone_text = 'Failed to clone the repository';
var failed_to_clone = $('<p class="help-block" id="failed_to_clone">' + failed_to_clone_text + '</p>');

function add_repository(url, deploy_key_container, on_success) {
    var request = $.get("/add_repository", {"url": url.val()});

    request.success(function (response) {
        var url_container = url.parent();

        console.log('Add repo');
        console.log(response);

        if(response.result == 'invalid repository') {
            url_container.addClass('has-error');
            failed_to_clone.insertAfter(url);
        } else {
            url.val("");
            url_container.removeClass('has-error');
            deploy_key_container.hide();
            on_success();
        }
    });

    request.error(function (jqXHR, textStatus, errorThrown) {
        if (textStatus == 'timeout')
            console.log('The server is not responding');

        if (textStatus == 'error')
            console.log(errorThrown);
    })
}

function show_deploy_key(deploy_key, deploy_key_container, on_success) {
    var request = $.get("/generate_deploy_key");

    request.success(function (response) {
        console.log('Show key');
        console.log(response);
        deploy_key_container.show();
        deploy_key.val(response.deploy_key);
        on_success();
    });

    request.error(function (jqXHR, textStatus, errorThrown) {
        if (textStatus == 'timeout')
            console.log('The server is not responding');

        if (textStatus == 'error')
            console.log(errorThrown);
    })
}

$(function () {
    var state = 0,
        deploy_key = $("#deploy_key"),
        deploy_key_container,
        url = $("#url"),
        url_container;

    deploy_key_container = deploy_key.parent();
    url_container = url.parent();

    deploy_key.attr('readonly', 'readonly');
    deploy_key_container.hide();

    function toggle_state() {state = 1 - state;}

    url.on('keyup paste', function () {
        if (state === 1) {
            failed_to_clone.remove();
            url_container.removeClass('has-error')
        }
    });

    $('#add_repository').submit(function (e) {
        e.preventDefault();

        if (state === 0) {
            show_deploy_key(deploy_key, deploy_key_container, toggle_state);
        } else if (state === 1) {
            add_repository(url, deploy_key_container, toggle_state);
        }

        return false;
    });
});
