function Repository(props) {
    return (
        <tr>
            <td>{props.url}</td>
            <td>{props.identity_file}</td>
        </tr>
    );
}

function RepositoryTableBody(props) {
    return (
        <tbody>
        {props.repositories.map(function (repo) {
            return <Repository
                key={repo.id}
                url={repo.url}
                identity_file={repo.identity_file}/>
        })}
        </tbody>
    )
}

function RepositoryTable(props) {
    return (
        <table id="repo_table" className="table table-striped">
            <thead>
            <tr>
                <th>URL</th>
                <th>Identity file</th>
            </tr>
            </thead>
            <RepositoryTableBody repositories={props.repositories}/>
        </table>
    )
}

function RepositoryList(props) {
    return (
        <div>
            <h2 className="header">Your repositories</h2>
            <RepositoryTable repositories={props.repositories}/>
        </div>
    )
}
