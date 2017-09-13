function render() {
        const tab_view = this;
        const tab = this.lookup[this.getCurrentTabId()];
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

function createLookup(arr) {
    let lookup = {};
        for (let i in arr) {
            const item = arr[i];
            lookup[item.id] = item;
        }
        return lookup;
}


class TabView extends React.Component {

    
    makeOnClick (tab) {
        const onClick = function () {
            this.props.set_current_tab(tab);
        }
        return onClick.bind(this);
    }
            
    constructor(props) {
        super(props);
        this.makeOnClick = this.makeOnClick.bind(this);
            

            this.getCurrentTabId = (function () {
                return this.props.current_tab_id;
            }).bind(this);

        

        this.lookup = createLookup(this.props.tabs);
          
    }

    render() {
        return render.call(this);
    }
}

class TabViewWithState extends React.Component {
    makeOnClick (tab) {
                const onClick = function () {
                    this.setState({
                        tab_id: tab.id
                    });
                };
                return onClick.bind(this);
            }

    constructor(props) {
        super(props);

        

            this.makeOnClick = this.makeOnClick.bind(this);

            this.state = {
                tab_id: props.initial_tab.id
            };

            this.getCurrentTabId = (function () {
                return this.state.tab_id
            }).bind(this);
        

        this.lookup = createLookup(this.props.tabs);
    }

    render() {
        return render.call(this);
    }
}

