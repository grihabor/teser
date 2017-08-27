
function RepositoryDeployKey(props) {

}

function RepositorySubmit(props) {
    return (
            <input className="btn btn-default" id="submit_button" name="submit_button" value="Add" type="submit" />
    )
}

function RepositoryAddForm(props) {
    return (
        <form id="add_repository">
            <RepositoryURL />
            <RepositoryDeployKey />
            <RepositorySubmit />
        </form>
    )
}

function RepositoryAdd(props) {
    return (
        <div>
            <h2 className="header">Add repository</h2>
            <RepositoryAddForm />
        </div>
    )
}

