# Team-3-Proton

| First Header  | Second Header |
| ------------- | ------------- |
| MrPersonManGuy  | Thomas Farrell  |
| Joseph Dumond  | Joseph Dumond  |
| Jacobghg  | Jacob Giangiulio  |
| Nrfuhrman  | Nathan Furhman |
| aneigh02  | Alec Neighbors |

# Note 1: We increased the allotted VB memory to 8 GB
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
 use:
 psql -d photon -U student
 \d players
 to connect to database as student and observe column names. (id, codename)

 The password field is set as student. I don't think thats what it is as defaut for the password, but i've changed it on my system so I dodn't know what it was.
 Use:
 \password student
 to update the password.

## Running the Game
To start the game, navigate to the project directory and run:

```bash
chmod +x install.sh
./install.sh
```

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


