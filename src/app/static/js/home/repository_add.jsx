function add_repository(url, onSuccess, onFailure, onError, onTimeout) {
    var request = $.get("/api/repository/add", {"url": url});

    request.success(function (response) {
        console.log('Add repo');
        console.log(response);

        if (response.result !== 'ok') {
            onFailure(response);
        } else {
            onSuccess(response);
        }
    });

    request.error(function (jqXHR, textStatus, errorThrown) {
        if (textStatus === 'timeout')
            console.log('The server is not responding');

        if (textStatus === 'error')
            console.log(errorThrown);
    })
}

function is_array(variable) {
    return Object.prototype.toString.call(variable) === '[object Array]';
}

function RepositoryURL(props) {
    let className = "form-group required",
        error_block = <div/>;

    if (props.has_error) {
        className += " has-error";
        error_block = (<p className="help-block raw-output" id="failed_to_clone">
            {is_array(props.error_details)
                ? props.error_details.map(function (line) {
                    return <p>{line}</p>;
                })
                : props.error_details}
        </p>)
    }
    return (
        <div className={className}>
            <label className="control-label">URL</label>
            <input className="form-control" id="url" name="url" required="" value={props.value} type="text"
                   onChange={props.onChange}/>
            {error_block}
            <p className="help-block">Example: user@gitlab.com:/user/project</p>
        </div>
    )
}

function show_deploy_key(onSuccess) {
    var request = $.get("/generate_deploy_key");

    request.success(function (response) {
        onSuccess(response);
    });

    request.error(function (jqXHR, textStatus, errorThrown) {
        if (textStatus == 'timeout')
            console.log('The server is not responding');

        if (textStatus == 'error')
            console.log(errorThrown);
    })
}

function RepositoryDeployKey(props) {
    return props.hidden ? <div/> : (
        <div className="form-group ">
            <label className="control-label">Public key</label>
            <textarea className="form-control" id="deploy_key" name="deploy_key" readOnly="readOnly"
                      value={props.value}/>
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
            hidden_key: true,
            key_value: "",
            error_details: "",
            has_error: false
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleURLChange = this.handleURLChange.bind(this);
    }

    handleURLChange(event) {
        event.preventDefault();

        this.setState({
            url_value: event.target.value,
            has_error: false
        });
    }

    handleSubmit(event) {
        console.log('A name was submitted: ' + this.state.value);
        event.preventDefault();
        if (this.state.hidden_key) {
            function onSuccess(response) {
                this.setState({
                    hidden_key: false,
                    key_value: response.deploy_key
                });
            }

            onSuccess = onSuccess.bind(this);
            show_deploy_key(onSuccess);

        } else {
            function onSuccess(response) {
                this.setState({
                    error_details: "",
                    has_error: false,
                    hidden_key: true,
                    url_value: ""
                });
                this.props.onAdd(response.repositories);
            }

            function onFailure(response) {
                this.setState({
                    error_details: response.details,
                    has_error: true
                });
            }

            onSuccess = onSuccess.bind(this);
            onFailure = onFailure.bind(this);

            add_repository(
                this.state.url_value,
                onSuccess,
                onFailure
            );
        }
    }

    render() {
        return (
            <form id="add_repository" onSubmit={this.handleSubmit}>
                <RepositoryURL
                    value={this.state.url_value}
                    error_details={this.state.error_details}
                    has_error={this.state.has_error}
                    onChange={this.handleURLChange}/>
                <RepositoryDeployKey
                    hidden={this.state.hidden_key}
                    value={this.state.key_value}/>
                <RepositorySubmit/>
            </form>
        )
    }
}

function RepositoryAdd(props) {
    return (
        <div>
            <h2 className="header">Add repository</h2>
            <RepositoryAddForm onAdd={props.onAdd}/>
        </div>
    )
}

