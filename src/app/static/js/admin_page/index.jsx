
class AdminPage extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            tab: 'user_list'
        }

        this.showTestingPanel = this.showTestingPanel.bind(this);
        this.showUserList = this.showUserList.bind(this);
        this.showActiveRepositoryList = this.showActiveRepositoryList.bind(this);
    }
    showUserList() {
        this.setState({tab: 'user_list'});
    }
    showTestingPanel() {
        this.setState({tab: 'testing_panel'});
    }
    showActiveRepositoryList() {
        this.setState({tab: 'active_repository_list'});
    }
    render() {
        let tab_content;
        if (this.state.tab === 'user_list') {
            tab_content = <UserList />;
        } else if (this.state.tab === 'testing_panel'){
            tab_content = <TestingPanel />;
        } else {
            tab_content = <ActiveRepositoryList />;
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
                <button onClick={this.showActiveRepositoryList}>
                    Active Repository List
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
