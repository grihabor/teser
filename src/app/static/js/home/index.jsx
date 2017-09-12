function load_repositories(onSuccess) {
    const request = $.get('/api/repository/list', {});

    request.success(function (response) {
        onSuccess(response.repositories);
    });
}

function remove_repository(repo_id, onSuccess) {
    const request = $.get('/api/repository/remove', {id: repo_id});

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
        this.handleRemove = this.handleRemove.bind(this);

        this.update_repositories();
    }

    handleRemove(repo_id) {
        console.log(repo_id);
        remove_repository(repo_id, this.set_repositories);
    }

    set_repositories(repositories) {
        console.log('Set repos: ' + repositories);
        this.setState({repositories: repositories});
    }

    update_repositories() {
        load_repositories(this.set_repositories);
    }

    render() {
        let admin_page = null;
        if (this.props.admin_page !== ""){
            admin_page = (
                <p className="screen-width">
                    Go to <a href={this.props.admin_page}>Admin page</a>
                </p>
            )
        }

        const page_content = (
            <div id="page_content">
                {admin_page}
                <h1 className="header screen-width">Home</h1>
                <RepositoryList repositories={this.state.repositories} onRemove={this.handleRemove} />
                <RepositoryAdd onAdd={this.set_repositories}/>
            </div>
        );
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
