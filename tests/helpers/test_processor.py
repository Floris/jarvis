from app.helpers.processor import parse_response
from tests.mocks.mocked import mocked_data


def test_parse_response():
    """Test the parse_response function."""
    response = """
    The project structure should look like this:

    # File: app/main.py
    def main():
        print("Hello, world!")
    // Done: app/main.py

    // File: app/__init__.py
    from .main import main

    ------- File: tests/test_main.py
    from app.main import main

    def test_main():
        main()
    """

    expected_output = [
        ("app", "main.py", '    def main():\n        print("Hello, world!")'),
        ("app", "__init__.py", "    from .main import main"),
        (
            "tests",
            "test_main.py",
            "    from app.main import main\n    def test_main():\n        main()",
        ),
    ]

    assert parse_response(response) == expected_output


def test_parse_response_mock_data():
    """Test the parse_response function."""

    expected_output = [
        (
            "public",
            "index.html",
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>FIXEX - The Best Cryptocurrency Exchange</title>\n"
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            "  </head>\n"
            "  <body>\n"
            '    <div id="root"></div>\n'
            '    <script src="../index.js"></script>\n'
            "  </body>\n"
            "</html>",
        ),
        (
            "",
            "package.json",
            "{\n"
            '  "name": "fixex-app",\n'
            '  "version": "1.0.0",\n'
            '  "dependencies": {\n'
            '    "react": "^17.0.2",\n'
            '    "react-dom": "^17.0.2",\n'
            '    "react-router-dom": "^5.2.0",\n'
            '    "react-scripts": "4.0.3",\n'
            '    "react-bootstrap": "^2.0.0-beta.4",\n'
            '    "bootstrap": "^5.1.0",\n'
            '    "react-icons": "^4.2.0",\n'
            '    "react-router-bootstrap": "^1.0.0-beta.10"\n'
            "  },\n"
            '  "scripts": {\n'
            '    "start": "react-scripts start",\n'
            '    "build": "react-scripts build",\n'
            '    "test": "react-scripts test",\n'
            '    "eject": "react-scripts eject"\n'
            "  }\n"
            "}",
        ),
        (
            "src",
            "App.js",
            "import React from 'react';\n"
            "import { Navbar, Nav, Button } from 'react-bootstrap';\n"
            "import { FaBitcoin, FaEthereum } from 'react-icons/fa';\n"
            "import { Link } from 'react-router-dom';\n"
            "import 'bootstrap/dist/css/bootstrap.min.css';\n"
            "import './App.css';\n"
            "function App() {\n"
            "  return (\n"
            '    <div className="App">\n'
            '      <Navbar bg="light" expand="lg">\n'
            '        <Navbar.Brand href="#home">FIXEX</Navbar.Brand>\n'
            '        <Navbar.Toggle aria-controls="basic-navbar-nav" />\n'
            '        <Navbar.Collapse id="basic-navbar-nav">\n'
            '          <Nav className="mr-auto">\n'
            '            <Link to="/" className="nav-link">Home</Link>\n'
            '            <Link to="/about" className="nav-link">About</Link>\n'
            '            <Link to="/contact" className="nav-link">Contact</Link>\n'
            "          </Nav>\n"
            "          <Nav>\n"
            '            <Button variant="primary" className="mr-2">Sign Up</Button>\n'
            "          </Nav>\n"
            "        </Navbar.Collapse>\n"
            "      </Navbar>\n"
            '      <header className="App-header">\n'
            "        <h1>Welcome to FIXEX</h1>\n"
            "        <p>Trade your favorite cryptocurrencies with ease.</p>\n"
            "        <ul>\n"
            "          <li><FaBitcoin /> Bitcoin</li>\n"
            "          <li><FaEthereum /> Ethereum</li>\n"
            "        </ul>\n"
            "      </header>\n"
            "    </div>\n"
            "  );\n"
            "}\n"
            "export default App;",
        ),
        (
            "",
            "index.js",
            "import React from 'react';\n"
            "import ReactDOM from 'react-dom';\n"
            "import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';\n"
            "import 'bootstrap/dist/css/bootstrap.min.css';\n"
            "import App from './App';\n"
            "ReactDOM.render(\n"
            "  <Router>\n"
            "    <Switch>\n"
            '      <Route exact path="/" component={App} />\n'
            "    </Switch>\n"
            "  </Router>,\n"
            "  document.getElementById('root')\n"
            ");",
        ),
    ]

    assert parse_response(mocked_data) == expected_output
