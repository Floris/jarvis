mocked_data = """
Here's the code to create a React web application for FIXEX, a cryptocurrency exchange:

// File: index.html
<!DOCTYPE html>
<html>
  <head>
    <title>FIXEX - The Best Cryptocurrency Exchange</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
  </head>
  <body>
    <div id="root"></div>
    <script src="bundle.js"></script>
  </body>
</html>

// File: package.json
{
  "name": "fixex-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-router-dom": "^5.2.0",
    "react-scripts": "4.0.3",
    "react-bootstrap": "^2.0.0-beta.4",
    "bootstrap": "^5.1.0",
    "react-icons": "^4.2.0",
    "react-router-bootstrap": "^1.0.0-beta.10"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}

// File: App.js
import React from 'react';
import { Navbar, Nav, Button } from 'react-bootstrap';
import { FaBitcoin, FaEthereum } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="#home">FIXEX</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/about" className="nav-link">About</Link>
            <Link to="/contact" className="nav-link">Contact</Link>
          </Nav>
          <Nav>
            <Button variant="primary" className="mr-2">Sign Up</Button>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <header className="App-header">
        <h1>Welcome to FIXEX</h1>
        <p>Trade your favorite cryptocurrencies with ease.</p>
        <ul>
          <li><FaBitcoin /> Bitcoin</li>
          <li><FaEthereum /> Ethereum</li>
        </ul>
      </header>
    </div>
  );
}

export default App;

// File: index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App';

ReactDOM.render(
  <Router>
    <Switch>
      <Route exact path="/" component={App} />
    </Switch>
  </Router>,
  document.getElementById('root')
);
"""
