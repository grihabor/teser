
class TabView extends React.Component {
    constructor(props) {
        let i,
            tab,
            onClick;
      
        function makeOnClick(tab) {
            onClick = function () {
                this.setState({
                    tab_id: tab.id
                });
            }
            return onClick.bind(this);
        }
        makeOnClick = makeOnClick.bind(this);
        
        for (i in props.tabs) {
            tab = props.tabs[i];
            tab.onClick = makeOnClick(tab);
        }
        
        super(props);
        this.state = {
            tab_id: props.initial_tab.id
        };
    }
    
    render() {
        const tab = this.props.tabs[this.state.tab_id];
        
        return (
            <div>
                <div>
                    {Object.keys(this.props.tabs).map(function(i) {
                        const tab_obj = this.props.tabs[i];
                        return (
                            <button onClick={tab_obj.onClick}>
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
