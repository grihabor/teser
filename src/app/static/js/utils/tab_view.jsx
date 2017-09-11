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
        
        this.lookup = {};
        for (let i in this.props.tabs) {
            const tab = this.props.tabs[i];
            this.lookup[tab.id] = tab;
        }
    }

    render() {
        const tab_view = this;
        const tab = this.lookup[this.state.tab_id];
        return (
            <div>
                <div>
                    {this.props.tabs.map(function (tab_obj) {
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
