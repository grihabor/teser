function RepositoryURL(props) {
    return (
        <div className="form-group required">
            <label className="control-label">URL</label>
            <input className="form-control" id="url" name="url" required="" value="" type="text"/>
            <p className="help-block">Example: user@gitlab.com:/user/project</p>
        </div>
    )
}
function RepositoryDeployKey(props) {
    return (
        <div className="form-group ">
            <label className="control-label">Public key</label>
            <textarea className="form-control" id="deploy_key" name="deploy_key" readOnly="" />
            <p className="help-block">Add this key to your project "Deploy keys"</p>
        </div>
    )
}

function RepositorySubmit(props) {
    return (
        <input className="btn btn-default" id="submit_button" name="submit_button" value="Add" type="submit"/>
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

