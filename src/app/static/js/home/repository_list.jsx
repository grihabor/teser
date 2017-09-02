function Repository(props) {
    return (
        <tr>
            <td>{props.url}</td>
            <td>{props.identity_file}</td>
            <td>
                <input
                    type="button"
                    onClick={props.onRemove}
                    value="Remove" />
            </td>
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
                identity_file={repo.identity_file}
                onRemove={function(){console.log(repo);props.onRemove(repo.id)}} />
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
                <th></th>
            </tr>
            </thead>
            <RepositoryTableBody repositories={props.repositories} onRemove={props.onRemove} />
        </table>
    )
}

function RepositoryList(props) {
    return (
        <div>
            <h2 className="header">Your repositories</h2>
            <RepositoryTable repositories={props.repositories} onRemove={props.onRemove} />
        </div>
    )
}
