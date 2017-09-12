
function TableViewBody(props) {
    return (
        <tbody>
        {
            props.items.map(function (item) {
                return <tr>
                    {props.columns.map(function (column_id) {
                        return item[column_id];
                    })}
                </tr>
            })
        }
        </tbody>
    )
}

class TableView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            items: []
        };
        this.set_items = this.set_items.bind(this);
        this.update_items = this.update_items.bind(this);

        this.update_items();
    }

    set_items(items) {
        this.setState({items: items});
    }

    update_items() {
        this.props.load_items(this.set_items);
    }

    render() {
        const name_mapping = this.props.name_mapping;
        return (
            <table className="table table-stripped">
                <thead>
                <tr>
                    {this.props.columns.map(function (column_id) {
                        return <th>{name_mapping[column_id]}</th>;
                    })}
                </tr>
                </thead>
                <TableViewBody
                    items={this.state.items}
                    columns={this.props.columns} />
            </table>
        )
    }
}

