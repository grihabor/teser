function read_logs() {

}

function run_tests(value) {

}

function load_active_repos(onSuccess) {
    const request = $.get('/api/repository/active/list', {});

    request.success(function (response) {
        onSuccess(response.active_repositories);
    });
}

function ActiveRepositoryList(props) {
    return (
        <div>
            <h2 className="header">Active Repository List</h2>
            <TableView items={[]}
                      load_items={load_active_repos}
                      columns={['id', 'url', 'run_tests']}
                      name_mapping={{
                          'id': 'Id',
                          'url': 'Url',
                          'run_tests': 'Run tests'
                      }}
                      buttons={{
                          'run_tests': {
                              onClick: run_tests,
                              value: function (repository) {
                                  return 'Run tests';
                              }
                          }
                      }}  />
        </div>
    )
}
