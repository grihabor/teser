
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
                      columns={['id', 'url']}
                      name_mapping={{
                          'id': 'Id',
                          'url': 'Url'
                      }}  />
        </div>
    )
}
