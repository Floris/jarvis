PROMPT_CODING_PORTFOLIO = """

* Project Name
Coding Portfolio

* Description
A responsive coding portfolio website showcasing projects, skills, and experiences.

* Programming Language
JavaScript, React

* Project Structure
coding-portfolio/
│
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
│
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── About.js
│   │   ├── Projects.js
│   │   ├── Skills.js
│   │   ├── Experience.js
│   │   └── Footer.js
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
│
├── .gitignore
├── README.md
├── LICENSE
├── package.json

* Dependencies
react (17.0.2)
react-dom (17.0.2)
react-router-dom (6.10.0)
react-scripts (5.0.1)
react-bootstrap (2.7.2)

* Bootstrap
Make sure bootstrap is installed and imported in the App.js file.

* Routing logic
Wrap the App component with the BrowserRouter component. Use the Link component from react-router-dom for navigation links.

* Theme
Implement a dark theme for the website using react-bootstrap's dark theme.

* Theme Toggle
Allow switching between light and dark themes using the ThemeProvider component from react-bootstrap.
Add this functionality to the navigation bar.

* Usage Instructions
npm start

* Test Instructions
npm test

* License
MIT License

* Notes
Make sure to generate code for all the files in the project structure.
Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.
# """


PROMPT_TRADING_BOT = """

* Project Name
Crypto Trading Bot

* Description
Crypto trading bot that uses the CCXT library to trade cryptocurrencies. This bot buys bitcoin by utilizing various indicators and strategies.
Implement a trading strategy that uses the RSI indicator to buy bitcoin when the RSI is below 30 and sell when the RSI is above 70.

* Programming Language
Python

* Project Structure
coding-portfolio/
│
├── app/
│   ├── __init__.py
│   ├── main.py
|
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│
├── .gitignore
├── README.md
├── LICENSE
├── pyproject.toml

* Dependencies
Use poetry to manage dependencies. Save the dependencies in the pyproject.toml file.

python = "^3.11"
pytest = "^7.2.2"
ccxt = "^3.0.57"

If more dependencies are needed, add them to the pyproject.toml file.

* Usage Instructions
python app/main.py

* Test Instructions
pytest

* License
MIT License

* Notes
Make sure to generate code for all the files in the project structure.
Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.
"""


PROMPT_API_CLIENT = """ 
* Project name?
generic api client

* Please provide a description of the project.
I am integrating an api into my python app. For this I need a api client. I think it is best to create a generic api client so I can easily integrate more in the future.

* Describe the technical aspects of the project.
Design this for me

* What programming languages will be used?
Python

* What packages/ dependencies will be used?
requests

* What package manager will be used? (pip, npm, etc.)
poetry

* What is the filename of the package manager file? (requirements.txt, package.json, etc.)
pyproject.toml

* Do you want us to provide the project structure?
yes please

* Do you want us to provide usage instructions for the project.
yes

* Do you want us to provide test instructions for the project.
Yes create some tests to show the functionalities created.

* Notes
Make sure to generate code for all the files in the project structure.
Please use 'File: {Project Name}/{path}/{filename}' as a tag for the file before the code block. And 'Done: {Project Name}/{path}/{filename}' as a tag for the file after the code block.
"""
