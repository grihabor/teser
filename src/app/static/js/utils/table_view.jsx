function TableViewBody(props) {
    const buttons = props.buttons;

    return (
        <tbody>
        {
            props.items.map(function (item) {
                return <tr key={item.id}>
                    {props.columns.map(function (column_id) {
                        const td_content = (function () {
                            if (buttons.hasOwnProperty(column_id)) {
                                const button = buttons[column_id];
                                return (
                                    <button onClick={function () {
                                        button.onClick(item)
                                    }}>
                                        {button.value(item)}
                                    </button>
                                );
                            }
                            return item[column_id];
                        })();
                        return <td key={column_id}>{td_content}</td>;
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
                <tr key="header_row">
                    {this.props.columns.map(function (column_id) {
                        return <th key={column_id}>{name_mapping[column_id]}</th>;
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

