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

class RepositoryTableBody extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            repositories: props.repositories
        };
    }

    update_repositories(repositories) {
        console.log('Loaded list: ' + repositories);
        console.log(this);
        this.state.repositories = repositories;
    }

    render() {
        let repo_list = [];
        for (let i in this.state.repositories) {
            const repo = this.state.repositories[i];
            repo_list.push(
                <Repository
                    key={repo.id}
                    url={repo.url}
                    identity_file={repo.identity_file}/>
            );
        }
        return <tbody>{repo_list}</tbody>
    }
}

function RepositoryTable(props) {
    return (
        <table id="repo_table" className="table table-striped">
            <thead>
            <tr>
                <th>URL</th>
                <th>Identity file</th>
            </tr>
            </thead>
            <RepositoryTableBody repositories={props.repositories}/>
        </table>
    )
}

function RepositoryList(props) {
    return (
        <div>
            <h2 className="header">Your repositories</h2>
            <RepositoryTable repositories={props.repositories}/>
        </div>
    )
}
