function AdminPage(props){
    return (
        <div id="page_content">
            <h1 className="header">Admin Page</h1>
        </div>
    )
}


(function () {
    const container = document.getElementById("page_container");
    ReactDOM.render(
        <AdminPage />,
        container
    );
})();