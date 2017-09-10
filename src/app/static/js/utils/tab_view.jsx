class TabView extends React.Component {

    makeOnClick(tab) {
        const onClick = function () {
            this.setState({
                tab_id: tab.id
            });
        };
        return onClick.bind(this);
    }

    constructor(props) {
        super(props);
        this.state = {
            tab_id: props.initial_tab.id
        };
    }

    render() {
        const tab_view = this;
        const tab = this.props.tabs[this.state.tab_id];
        return (
            <div>
                <div>
                    {Object.keys(this.props.tabs).map(function (i) {
                        const tab_obj = tab_view.props.tabs[i];
                        return (
                            <button key={tab_obj.id}
                                    onClick={tab_view.makeOnClick(tab_obj)}>
                                {tab_obj.title}
                            </button>
                        )
                    })}
                </div>
                {tab.content}
            </div>
        )
    }
}
