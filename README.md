# Coffee_shop_FullStack

The Coffee_shop_FullStack project is the 3rd project in the FullStack Nano Degree offered by UDACITY. The focus of the project is to apply what is learned in the Identity and Access Management section using FLASK framework and Auth0

## Project Description

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

## About the Stack

The key functional areas:

### Backend

The `./backend` directory contains a Flask server with an SQLAlchemy module that was pre-written.I implemented the endpoints, configuration , and integration Auth0 for authentication and authorization.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. I update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
