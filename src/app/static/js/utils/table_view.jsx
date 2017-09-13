function TableViewBody(props) {
    const buttons = props.buttons;

    return (
        <tbody>
        {
            props.items.map(function (item) {
                return <tr>
                    {props.columns.map(function (column_id) {
                        if (buttons.hasOwnProperty(column_id)) {
                            const button = buttons[column_id];
                            return (
                                <td><button onClick={function () {
                                    button.onClick(item)
                                }}>
                                    {button.value(item)}
                                </button></td>
                            );
                        }
                        return <td>{item[column_id]}</td>;
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

        if (!props.hasOwnProperty('buttons')) {
            this.buttons = {};
        } else {
            this.buttons = props.buttons;
        }

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
                    buttons={this.buttons}
                    columns={this.props.columns}/>
            </table>
        )
    }
}

