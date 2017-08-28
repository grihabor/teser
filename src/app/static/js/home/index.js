class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state({
            repositories = []
        });
        this.add_repository.bind(this);
    },
    add_repository(reposittory) {
        console.log('Add repo: ' + repository);
    },
    render() {
        return (
            <div id="page_content">
                <h1 id="home_header" className="header">Home</h1>
                <RepositoryList repositories={props.repositories}/>
                <RepositoryAdd onAdd={this.add_repository}/>
            </div>
        )
    }
}


function main() {
    load_repositories(function (repositories) {
        ReactDOM.render(
            <HomePage repositories={repositories}/>,
            document.getElementById("page_container")
        );
    });

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

    function update_repository_list(repositories) {
        var i,
            repo,
            table_body = $('#repo_table > tbody'),
            new_body = $('<tbody></tbody>'),
            row,
            item;

        for (i in repositories) {
            repo = repositories[i];
            row = $('<tr></tr>');
            row.append('<td>' + repo.url + '</td>');
            row.append('<td>' + repo.identity_file + '</td>');
            new_body.append(row);
        }

        table_body.html(new_body.html());
    }

    function add_repository() {
        var request = $.get("/api/repository/add", {"url": url.val()});

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
                update_repository_list(response.repositories);
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
}

main();
