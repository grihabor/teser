
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
