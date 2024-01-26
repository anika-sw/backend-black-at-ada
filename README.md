# Black@Ada web app (backend)

Black@Ada is a member-only web application fostering community by creating a digital space just for Black Adies. It's dynamic and can grow as the number of Black Adies increases, and it's virtual nature means that it can be used by any Black Adie anywhere.

[Capstone Presentation](https://youtu.be/kOpsiBWTm48)

[Frontend Repository](https://github.com/anika-sw/frontend-black-at-ada)

## Application Features

### Technologies

This project utilizes Flask with PostgreSQL. Flask-Bcrypt allows for user passwords to be hashed and stored securely in the database.

### Models & Routes

Three models (and their tables) represent a many-to-many association for Black@Ada data: Event, User, and Event_User. Each event can have multiple user attendees, and each user can attend multiple events. In addition to routes for established event and user data, there are also routes to authenticate users at sign-up and login, and a route to handle image data transferred between the app's frontend and Google Cloud Storage.

### Dependencies

* API keys for:
  *  Google Maps API
  *  LocationIQ API. Keys are stored in the .env file for security.