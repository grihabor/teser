class Logs extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let logs;
        if (Array.isArray(this.props.logs)) {
            logs = this.props.logs.map(function (line) {
                console.log(line);
                const logStyle = {color: line.color};
                return <p style={logStyle}>{line.text}</p>;
            });
        } else {
            logs = this.props.logs;
        }
        return (
            <div>
                <h2 className="header">Logs</h2>
                <div>{logs}</div>
            </div>
        );
    }
}

class AdminPage extends React.Component {
    constructor(props) {
        super(props);
        this.show_logs = this.show_logs.bind(this);
        this.set_current_tab = this.set_current_tab.bind(this);

        this.state = {
            current_tab_id: 'user_list',
            logs: [{text: 'Log is empty', color: 'black'}]
        };

        this.tabs = [
            {
                id: 'user_list',
                title: 'User List',
                content: <UserList/>
            }, {
                id: 'active_repository_list',
                title: 'Active Repositories',
                content: <ActiveRepositoryList show_logs={this.show_logs}/>
            }, {
                id: 'testing_panel',
                title: 'Testing Panel',
                content: <TestingPanel/>
            }
        ];
    }

    show_logs(details) {
        console.log(details);
        this.setState({
            current_tab_id: 'logs',
            logs: details
        })
    }

    set_current_tab(tab) {
        this.setState({
            current_tab_id: tab.id
        })
    }

    render() {
        const logs_tab = {
            id: 'logs',
            title: 'Logs',
            content: <Logs logs={this.state.logs}/>
        };
        const tabs = this.tabs.concat([logs_tab]);
        return (
            <div>
                <p className="screen-width">
                    Back to <a href={this.props.home_page}>Home page</a>
                </p>

                <TabView
                    current_tab_id={this.state.current_tab_id}
                    set_current_tab={this.set_current_tab}
                    tabs={tabs}/>
            </div>
        )
    }
}


(function () {
    const container = document.getElementById("page_container");
    const home_page = container.getAttribute('data-home-page');
    ReactDOM.render(
        <AdminPage home_page={home_page}/>,
        container
    );
})();
