class TabView extends React.Component {

    constructor(props) {
        super(props);

        if (props.hasOwnProperty('set_current_tab')) {

            this.makeOnClick = (function (tab) {
                return props.set_current_tab(tab);
            }).bind(this);

            this.currentTabId = (function () {
                return props.current_tab_id;
            }).bind(this);

        } else {

            this.makeOnClick = (function (tab) {
                const onClick = function () {
                    this.setState({
                        tab_id: tab.id
                    });
                };
                return onClick.bind(this);
            }).bind(this);

            this.state = {
                tab_id: props.initial_tab.id
            };

            this.currentTabId = (function () {
                return this.state.tab_id
            }).bind(this);
        }

        this.lookup = {};
        for (let i in this.props.tabs) {
            const tab = this.props.tabs[i];
            this.lookup[tab.id] = tab;
        }
    }

    render() {
        const tab_view = this;
        const tab = this.lookup[this.currentTabId()];
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

