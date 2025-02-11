# Team-3-Proton
# Repository made by Nathan Fuhrman
# Note 1: We increased the allotted VB memory to 8 GB


 install psycopg2(Python postgreSQL adapter):
 pip install psycopg2-binary

 use:
 psql -d photon -U student
 \d players
 to connect to database as student and observe column names. (id, codename)

 The password field is set as student. I don't think thats what it is as defaut for the password, but i've changed it on my system so I dodn't know what it was.
 Use:
 \password student
 to update the password.

 In the main() first checks if there is a player with ID 1, which in fact there is: "Opus", unsure what to do about him. You can change the vT value from 1 to 2 for example to get it to print a new id & name.


 # Laser Tag Game - Player Entry Screen


## Prerequisites
Before running the game, ensure you have the following installed:

### Required Python Version
- Python 3.8 or later

### Install Dependencies
Run the following command to install the required Python libraries:

```bash
pip install pygame psycopg2
```

### Database Setup
The game connects to a PostgreSQL database. Ensure you have a PostgreSQL database set up with the following details:

- Database Name: `photon`
- User: `student`
- Password: `student`
- Host: `localhost`

The database must contain a table `players` with at least the following columns:

```sql
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    codename VARCHAR(255) NOT NULL
);
```

## Running the Game
To start the game, navigate to the project directory and run:

```bash
python main.py
```

## Controls
- **Arrow Keys**: Navigate between players
- **TAB**: Switch between Red and Green teams
- **F1**: Edit game settings
- **F2**: Configure game parameters
- **F3**: Start the game
- **F7**: Create a new game
- **F12**: Clear the current game setup

## Features
- Query and insert player details into a PostgreSQL database
- Interactive UI with a team selection system
- Gradient backgrounds and button-based navigation
- Error handling for database operations

## Notes
- Ensure PostgreSQL is running before launching the game.
- The `logo.jpg` file must be present in the same directory as `main.py` for the splash screen to work.


