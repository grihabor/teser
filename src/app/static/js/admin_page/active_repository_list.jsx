function read_logs() {

}

function run_tests(repository, onSuccess) {
    const request = $.get('/api/task/start', {
        repository_id: repository.id
    });

    request.success(function (response) {
        onSuccess(response.details);
    });
}

function load_active_repos(onSuccess) {
    const request = $.get('/api/repository/active/list', {});

    request.success(function (response) {
        onSuccess(response.active_repositories);
    });
}

class ActiveRepositoryList extends React.Component {
    constructor(props) {
        super(props);
        this.columns = ['id', 'url', 'run_tests'];
        this.name_mapping = {
            'id': 'Id',
            'url': 'Url',
            'run_tests': 'Run tests'
        };
        this.buttons = {
            'run_tests': {
                onClick: function (item) {
                    run_tests(item, props.show_logs)
                },
                value: function (repository) {
                    return 'Run tests';
                }
            }
        };
    }


    render() {
        return (
            <div>
                <h2 className="header">Active Repository List</h2>
                <TableView items={[]}
                           load_items={load_active_repos}
                           columns={this.columns}
                           name_mapping={this.name_mapping}
                           buttons={this.buttons}/>
            </div>
        )
    }
}






