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
            </tr>
        })}
        </tbody>
    )
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
            <h2 className="header">User List</h2>
            <UserTable/>
        </div>
    )
}

function AdminPage(props) {
    return (
        <div>
            <p className="screen-width">Back to <a href={props.home_page}>Home page</a></p>
            <div id="page_content">
                <h1 className="header screen-width">Admin Page</h1>
                <UserList/>
            </div>
        </div>
    )
}


(function () {
    const container = document.getElementById("page_container");
    const home_page = container.getAttribute('data-home-page');
    ReactDOM.render(
        <AdminPage home_page={home_page}/>,
        container
    );
})();
