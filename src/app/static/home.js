$(function () {
    var state = 0,
        deploy_key = $("#deploy_key"),
        url = $("#url");


    deploy_key.attr('readonly', 'readonly');

    function failed_to_clone(text) {
        return $('<p class="help-block" id="failed_to_clone">' + text + '</p>');
    }

    function toggle_state() {
        state = 1 - state;
    }

    function add_repository() {
        var request = $.get("/add_repository", {"url": url.val()});

        request.success(function (response) {
            var url_container = url.parent();

            console.log('Add repo');
            console.log(response);

            if (response.result != 'ok') {
                url_container.addClass('has-error');
                $("#failed_to_clone").remove();
                failed_to_clone(response.details).insertAfter(url);
            } else {
                url.val("");
                url_container.removeClass('has-error');
                deploy_key.parent().hide();
                $('#failed_to_clone').remove();
                toggle_state();
            }
        });

        request.error(function (jqXHR, textStatus, errorThrown) {
            if (textStatus == 'timeout')
                console.log('The server is not responding');

            if (textStatus == 'error')
                console.log(errorThrown);
        })
    }

    function show_deploy_key() {
        var request = $.get("/generate_deploy_key");

        request.success(function (response) {
            console.log('Show key');
            console.log(response);
            deploy_key.parent().show();
            deploy_key.val(response.deploy_key);
            toggle_state();
        });

        request.error(function (jqXHR, textStatus, errorThrown) {
            if (textStatus == 'timeout')
                console.log('The server is not responding');

            if (textStatus == 'error')
                console.log(errorThrown);
        })
    }

    url.on('keyup paste', function () {
        if (state === 1) {
            $('#failed_to_clone').remove();
            url.parent().removeClass('has-error');
        }
    });

    $('#add_repository').submit(function (e) {
        e.preventDefault();

        if (state === 0) {
            show_deploy_key();
        } else if (state === 1) {
            add_repository();
        }

        return false;
    });
});
