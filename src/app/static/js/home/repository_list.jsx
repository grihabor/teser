function Repository(props) {
    let is_active_class = '';
    if (props.is_active) {
        is_active_class = "active-repository";
    }
    return (
        <tr className={is_active_class}>
            <td>{props.url}</td>
            <td>{props.identity_file}</td>
            <td>
                <input
                    className="btn btn-danger"
                    type="button"
                    onClick={props.onRemove}
                    value="Remove"/>
            </td>
            <td>
                <input
                    className="btn btn-default"
                    type="button"
                    onClick={props.onActivate}
                    value="Activate"/>
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
                is_active={repo.is_active}
                onRemove={function () {
                    props.onRemove(repo.id)
                }}
                onActivate={function () {
                    props.onActivate(repo.id)
                }}/>
        })}
        </tbody>
    )
}

function RepositoryTable(props) {
    return (
        <table id="repo_table" className="table">
            <thead>
            <tr>
                <th>URL</th>
                <th>Identity file</th>
                <th></th>
            </tr>
            </thead>
            <RepositoryTableBody
                repositories={props.repositories}
                onRemove={props.onRemove}
                onActivate={props.onActivate}/>
        </table>
    )
}

function RepositoryList(props) {
    return (
        <div>
            <h2 className="header">Your repositories</h2>
            <RepositoryTable
                repositories={props.repositories}
                onRemove={props.onRemove}
                onActivate={props.onActivate}/>
        </div>
    )
}
