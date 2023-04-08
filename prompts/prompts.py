# prompt = (
#     "Create a Python project structure and code for a simple calculator with add, subtract, multiply, and divide functions. Also create tests for this calculator."
#     " The project should have a 'src' folder with a 'calculator.py' file."
#     " The project also should have a 'tests' folder with a 'test_calculator.py' file."
#     " Provide the project structure and code for the 'calculator.py' file & 'test_calculator.py' file."
#     "\n# calculator.py\n# test_calculator.py"
# )
# prompt = """
# Create a Django DRF (Django Rest Framework) application that allows users to create, read, update, and delete data for a given model. The application should include the following components:

# 1. A model with the following fields:
#     - id (auto-incrementing integer)
#     - name (string)
#     - description (text)
#     - created_at (datetime)
#     - updated_at (datetime)

# 2. A serializer that can convert the model instance to JSON and vice versa.

# 3. Views for handling CRUD operations for the model.

# 4. URL patterns that map to the appropriate views.

# 5. A database to store the model data.

# 6. Authentication and authorization to restrict access to the views.

# Please write the necessary code to implement the above requirements. Make sure to include any necessary dependencies and installation instructions in the code comments.

# Tag files by using 'File: path+filename'.
# """
# When referencing a file, use the following format: 'File: path+filename'
# Tag files by using 'File: path+filename'.

# project_name = "django_app"


PROMPT_NAME = "landingpage"
PROMPT = """Develop a modern website using React and Bootstrap for FIXEX, a cryptocurrency exchange. The website should have a sleek dark mode design and be fully responsive for desktop and mobile devices.

The landing page should be a static page with the following sections:

A navigation bar at the top with links to different sections of the page.
Section 1: A banner with a background image and a call-to-action button to sign up for an account.
Section 2: A brief description of the website.
Section 3: A list of supported cryptocurrencies and trading pairs.
Section 4: A call-to-action button to sign up for an account.
Section 5: A footer with links to social media and other relevant pages.
The header and footer should have a flat green linear gradient background.

To implement this, you should create the necessary HTML tags to render the React application in an index.html file located in 'public/index.html'. Also, you should add index.js and App.js files to the project and render the App component in the index.js file. 
Please make sure to install the necessary dependencies for the project, including react, react-dom, react-router-dom, react-scripts, react-bootstrap, bootstrap, and react-icons.

To add a styled navigation in Bootstrap, you can use the Navbar component from react-bootstrap. 
You can create a Navbar with links to different sections of the page, and style it to fit the dark mode design. 
You can also use the NavDropdown component to create dropdown menus for the navigation links.

# Please write the necessary code to implement the above requirements. Make sure to include any necessary dependencies.
# Don't include installation instructions.

Please use 'File: path+filename' to tag the files containing the necessary code to complete this task.
"""
