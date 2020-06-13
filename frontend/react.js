
const e = React.createElement;
const alert = Reactstrap.Alert

class Page extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return e(alert,{'color':"danger"},e(alert,{'color':"danger"},"ok"))
  }
}

const domContainer = document.querySelector('#app');
ReactDOM.render(e(Page), domContainer);
