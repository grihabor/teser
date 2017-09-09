
class TabView extends React.Component {
    constructor(props) {
        let i,
            tab,
            onClick,
            patched_tabs = [];
        
        function makeOnClick(tab) {
            function onClick() {
                this.setState({
                    tab_id: tab.id
                });
            }
            return onClick.bind(this);
        }
        makeOnClick = makeOnClick.bind(this);
        
        for (i in props.tabs) {
            tab = props.tabs[i];
            tab.onClick = makeOnClick(tab);
        }
        
        super(props);
        this.state = {
            tab_id: props.initial_tab.id
        };
    }
    
    render() {
        const tab = this.props.tabs[this.tab_id];
        const tab_content = tab.content;
        return (
            <div>
                <div>
                    {this.props.tabs.map(function(tab) {
                        return (
                            <button onClick={tab.onClick}>
                                {tab.title}
                            </button>
                        )
                    })}
                </div>
                {tab_content}
            </div>
        )
    }
}

class AdminPage extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            tab: 'user_list'
        }
        
    }
    
    render() {
        const tabs = {
            user_list: {
                id: 'user_list',
                content: <UserList />
            }, testing_panel: {
                id: 'testing_panel',
                content: <TestingPanel />
            }, active_repository_list: {
                id: 'active_repository_list',
                content: <ActiveRepositoryList />
            }, smth: {
                id: 'smth',
                content: <div>smth</div>
            }
        };
        return (
            <div>
                <p className="screen-width">
                    Back to <a href={this.props.home_page}>Home page</a>
                </p>
            
                <TabView tabs={tabs} />
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
