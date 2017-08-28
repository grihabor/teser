
function RepositoryURL(props) {
    return (
        <div className="form-group required">
            <label className="control-label">URL</label>
            <input className="form-control" id="url" name="url" required="" value={props.value} type="text" onChange={props.onChange}/>
            <p className="help-block">Example: user@gitlab.com:/user/project</p>
        </div>
    )
}

function RepositoryDeployKey(props) {
    return props.hidden ? <div /> : (
        <div className="form-group ">
            <label className="control-label">Public key</label>
            <textarea className="form-control" id="deploy_key" name="deploy_key" readOnly="readOnly"/>
            <p className="help-block">Add this key to your project "Deploy keys"</p>
        </div>
    )
}

function RepositorySubmit(props) {
    return (
        <input
            className="btn btn-default"
            value="Add"
            type="submit"/>
    )
}

class RepositoryAddForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            url_value: "",
            hidden_key: true
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleURLChange = this.handleURLChange.bind(this);
    }

    handleURLChange(event) {
        event.preventDefault();

        this.setState({
            url_value: event.target.value
        });
    }

    handleSubmit(event) {
        console.log('A name was submitted: ' + this.state.value);
        event.preventDefault();
alert();
    }

    render() {
        return (
            <form id="add_repository">
                <RepositoryURL value={this.state.url_value} onChange={this.handleURLChange}/>
                <RepositoryDeployKey hidden={this.state.hidden_key}/>
                <RepositorySubmit />
            </form>
        )
    }
}

function RepositoryAdd(props) {
    return (
        <div>
            <h2 className="header">Add repository</h2>
            <RepositoryAddForm />
        </div>
    )
}

