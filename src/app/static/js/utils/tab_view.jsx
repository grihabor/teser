function searchForId(arr, id) {
    let i,
        item;
    for (i in arr) {
        item = arr[i];
        if (item.id === id) {
            return item;
        }
    }
    return null;
}

function render() {
    const tab_view = this;
    const tab = searchForId(
        this.props.tabs,
        this.getCurrentTabId()
    );
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


class TabView extends React.Component {

    makeOnClick(tab) {
        const onClick = function () {
            this.props.set_current_tab(tab);
        };
        return onClick.bind(this);
    }

    getCurrentTabId() {
        return this.props.current_tab_id;
    }


    constructor(props) {
        super(props);
        this.makeOnClick = this.makeOnClick.bind(this);
        this.getCurrentTabId = this.getCurrentTabId.bind(this);
    }

    render() {
        return render.call(this);
    }
}

class TabViewWithState extends React.Component {

    makeOnClick(tab) {
        const onClick = function () {
            this.setState({
                tab_id: tab.id
            });
        };
        return onClick.bind(this);
    }

    getCurrentTabId() {
        return this.state.tab_id;
    }

    constructor(props) {
        super(props);

        this.makeOnClick = this.makeOnClick.bind(this);
        this.getCurrentTabId = this.getCurrentTabId.bind(this);

        this.state = {
            tab_id: props.initial_tab.id
        };
    }

    render() {
        return render.call(this);
    }
}

