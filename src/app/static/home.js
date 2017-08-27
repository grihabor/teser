function Repository(props) {
    return (
        <tr>
            <td>{props.url}</td>
            <td>{props.identity_file}</td>
        </tr>
    );
}

function load_repositories(onSuccess) {
    let repositories;
    const request = $.get('/api/repository/list', {});

    request.success(function (response) {
        onSuccess(response.repositories);
    });
}

class RepositoryList extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            repositories: []
        };

        load_repositories(function(repositories){
            this.state.repositories = repositories;
        });
    }

    render() {
        let repo_list = [];
        for (let i in this.state.repositories) {
            const repo = this.state.repositories[i];
            repo_list.push(
                <Repository
                    url={repo.url}
                    identity_file={repo.identity_file}/>
            );
        }
        return <tbody>{repo_list}</tbody>
    }
}


function main() {
    ReactDOM.render(
        <RepositoryList/>,
        document.getElementById("repository_list")
    );

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
