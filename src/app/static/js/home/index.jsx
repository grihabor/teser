function load_repositories(onSuccess) {
    const request = $.get('/api/repository/list', {});

    request.success(function (response) {
        onSuccess(response.repositories);
    });
}


class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            repositories: []
        };
        this.set_repositories = this.set_repositories.bind(this);
        this.update_repositories = this.update_repositories.bind(this);

        this.update_repositories();
    }

    set_repositories(repositories) {
        console.log('Set repos: ' + repositories);
        this.setState({repositories: repositories});
    }

    update_repositories() {
        load_repositories(this.set_repositories);
    }

    render() {
        const page_content = (
            <div id="page_content">
                <h1 className="header screen-width">Home</h1>
                <RepositoryList repositories={this.state.repositories}/>
                <RepositoryAdd onAdd={this.set_repositories}/>
            </div>
        );
        if (this.props.admin_page !== ""){
            return (
                <div>
                    <p className="screen-width">Go to <a href={this.props.admin_page}>Admin page</a></p>
                    {page_content}
                </div>
            )
        } else {
            return page_content;
        }
    }
}


(function main() {
    const container = document.getElementById("page_container");
    const admin_page = container.getAttribute('data-admin-page');
    ReactDOM.render(
        <HomePage admin_page={admin_page}/>,
        container
    );
})();

/*{

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
*/
