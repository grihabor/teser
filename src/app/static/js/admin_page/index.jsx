function AdminPage(props) {
    const tabs = [
        {
            id: 'user_list',
            title: 'User List',
            content: <UserList/>
        }, {
            id: 'active_repository_list',
            title: 'Active Repositories',
            content: <ActiveRepositoryList/>
        }, {
            id: 'testing_panel',
            title: 'Testing Panel',
            content: <TestingPanel/>
        }
    ];
    return (
        <div>
            <p className="screen-width">
                Back to <a href={props.home_page}>Home page</a>
            </p>

            <TabView
                tabs={tabs}
                initial_tab={tabs[0]}/>
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
