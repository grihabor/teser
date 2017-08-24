function add_repository(url, deploy_key_container, on_success) {
    var request = $.get("/add_repository", {"url": url.val()});

    request.success(function (response) {
        console.log('Add repo');
        console.log(response);

        if(response.result == 'invalid repository') {
            var url_container = url.parent();
            url_container.addClass('has-error');
        } else {
            url.val("");
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
        url = $("#url");

    deploy_key_container = deploy_key.parent();

    deploy_key.attr('readonly', 'readonly');
    deploy_key_container.hide();

    function toggle_state() {state = 1 - state;}


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
