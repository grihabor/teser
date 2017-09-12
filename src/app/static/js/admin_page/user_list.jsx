function load_users(onSuccess) {
    const request = $.get('/api/user/list', {});

    request.success(function (response) {
        onSuccess(response.users);
    });
}

function UserTableBody(props) {
    return (
        <tbody>
        {props.users.map(function (user) {
            return <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.email}</td>
                <td>{user.username}</td>
                <td>{user.roles}</td>
            </tr>
        })}
        </tbody>
    )
}

function TableViewBody(props) {
    return (
        <tbody>
        {
            props.items.map(function (item) {
                return <tr>
                    {props.columns.map(function (column_id) {
                        return item[column_id];
                    })}
                </tr>
            })
        }
        </tbody>
    )
}

class TableView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: []
        };
        this.set_items = this.set_items.bind(this);
        this.update_items = this.update_items.bind(this);

        this.update_items();
    }

    set_items(items) {
        this.state({items: items});
    }

    update_items() {
        this.props.load_items(this.set_items);
    }

    render() {
        const name_mapping = this.props.name_mapping;
        return (
            <table className="table table-stripped">
                <thead>
                <tr>
                    {this.props.columns.map(function (column_id) {
                        return <th>{name_mapping[column_id]}</th>;
                    })}
                </tr>
                </thead>
                <TableViewBody
                    items={this.state.items}
                    columns={this.props.columns} />
            </table>
        )
    }
}

class UserTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            users: []
        };

        this.set_users = this.set_users.bind(this);
        this.update_users = this.update_users.bind(this);

        this.update_users();
    }

    set_users(users) {
        this.setState({users: users});
    }

    update_users() {
        load_users(this.set_users);
    }

    render() {
        return (
            <table className="table table-stripped">
                <thead>
                <tr>
                    <th>Id</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Roles</th>
                </tr>
                </thead>
                <UserTableBody users={this.state.users}/>
            </table>
        )
    }
}

function UserList(props) {
    return (
        <div>
            <h2 className="header">
                User List
            </h2>
            <UserTable/>
        </div>
    )
}
