
class TabView extends React.Component {
    constructor(props) {
        let i,
            tab,
            onClick;
      
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
        const tab = this.props.tabs[this.state.tab_id];
        
        return (
            <div>
                <div>
                    {Object.keys(this.props.tabs).map(function(i) {
                        const tab_obj = this.props.tabs[i];
                        return (
                            <button onClick={tab_obj.onClick}>
                                {tab_obj.title}
                            </button>
                        )
                    })}
                </div>
                {tab.content}
            </div>
        )
    }
}

def AdminPage (props) {
        const tabs = {
            user_list: {
                id: 'user_list',
                title: 'User List',
                content: <UserList />
            }, testing_panel: {
                id: 'testing_panel',
                title: 'Testing Panel',
                content: <TestingPanel />
            }, active_repository_list: {
                id: 'active_repository_list',
                title: 'Active Repositories',
                content: <ActiveRepositoryList />
            }, smth: {
                id: 'smth',
                title: 'Smth',
                content: <div>smth</div>
            }
        };
        return (
            <div>
                <p className="screen-width">
                    Back to <a href={props.home_page}>Home page</a>
                </p>
            
                <TabView 
                    tabs={tabs} 
                    initial_tab={tabs.user_list} />
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
