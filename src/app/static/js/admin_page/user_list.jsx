function load_users(onSuccess) {
    const request = $.get('/api/user/list', {});

    request.success(function (response) {
        onSuccess(response.users);
    });
}

function UserList(props) {
    return (
        <div>
            <h2 className="header">
                User List
            </h2>
            <TableView items={[]}
                       load_items={load_users}
                       columns={[
                           'id',
                           'email',
                           'username',
                           'roles'
                       ]}
                       name_mapping={{
                           'id': 'Id',
                           'email': 'Email',
                           'username': 'Username',
                           'roles': 'Roles'
                       }}/>
        </div>

    )
}
