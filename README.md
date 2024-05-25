# Workout Tracker Web Application

## Description
A simple web app to log and display workouts using Flask for the backend and React for the frontend

## Dependencies
- Python 3.8.2
- Node.js v20.13.1
- npm 10.5.2

## Backend setup

1. Clone the repository and enter backend

2. Create virtual environment using venv and activate
```sh
    python3 -m venv venv
    source venv/bin/activate
```

3. Install python packages
 ```sh
    pip install -r requirements.txt
 ```

4. Set up the DB 

 ```sh
    flask shell
    db.create_all()
  ```

5. Run the backend
 ```sh
    python app.py
 ```

## Frontend Setup

1. Navigate the frontend directory

2. Install needed npm packages
 ```sh
    npm install
 ``` 

3. Start the React dev server
 ```sh
    npm start
  ```

Enjoy your workout! 
