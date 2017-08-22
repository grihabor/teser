function add_repository(url, deploy_key_container) {
    var request = $.get("/add_repository", {"url": url.val()});

    request.success(function (response) {
        console.log('Add repo');
        console.log(response);
        url.val("");
        deploy_key_container.hide();
    });

    request.error(function (jqXHR, textStatus, errorThrown) {
        if (textStatus == 'timeout')
            console.log('The server is not responding');

        if (textStatus == 'error')
            console.log(errorThrown);
    })
}

function show_deploy_key(deploy_key, deploy_key_container) {
    var request = $.get("/generate_deploy_key");

    request.success(function (response) {
        console.log('Show key');
        console.log(response);
        deploy_key_container.show();
        deploy_key.val(response.deploy_key);
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

    $('#add_repository').submit(function (e) {
        e.preventDefault();

        if (state === 0) {
            show_deploy_key(deploy_key, deploy_key_container);
        } else if (state === 1) {
            add_repository(url, deploy_key_container);
        }
        state = 1 - state;

        return false;
    });
});
