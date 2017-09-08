

function TestingPanel(props) {
    return (
        <h3>Testing panel</h3>
    )
}

class AdminPage extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            tab: 'user_list'
        }

        this.showTestingPanel = this.showTestingPanel.bind(this);
        this.showUserList = this.showUserList.bind(this);
    }
    showUserList() {
        this.setState({tab: 'user_list'});
    }
    showTestingPanel() {
        this.setState({tab: 'testing_panel'});
    }
    render() {
        let tab_content;
        if (this.state.tab === 'user_list') {
            tab_content = <UserList />;
        } else {
            tab_content = <TestingPanel />;
        }
        return (
        <div>
            <p className="screen-width">
                Back to <a href={this.props.home_page}>Home page</a>
            </p>
            
            <div id="page_content">
                <h1 className="header screen-width">
                    Admin Page
                </h1>
                <div>
                <button onClick={this.showUserList}>
                    User List
                </button>
                <button onClick={this.showTestingPanel}>
                    Testing Panel
                </button>
                </div>
                {tab_content}
            </div>
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
