# Team-3-Proton

| Github Users | Names |
| ------------- | ------------- |
| MrPersonManGuy  | Thomas Farrell  |
| Joseph-Dumond  | Joseph Dumond  |
| Jacobghg  | Jacob Giangiulio  |
| nrfuhrman  | Nathan Fuhrman |
| aneigh02  | Alec Neighbors |

# Note 1: We increased the allotted VB memory to 8 GB
# Note 2: The VB's audio drivers seem to have some issues when being run on a Macbook, in our case it was an intel Macbook Pro. We recommend using a windows machine to run this program in a Debian Virtual Box.

## Running the Game
To install the necessary packages navigate to the project directory and run:

```bash
chmod +x install.sh
./install.sh
```

If you have problems with the install file, try running the following commands independently instead:

To install pip:
```bash
sudo apt install python3-pip
```

To install psycopg2:
```bash
python3 -m pip install psycopg2-binary
```

To install pygame:
```bash
python3 -m pip install pygame==2.6.1
```

Now to run the application use:

```bash
python3 main.py
```

## Controls
- **Up and Down Arrow Keys**: Navigate between players
- **TAB**: Switch between Red and Green teams
  - **Note**: It will jump to the highest unfilled row, or if all are filled it will jump up to the top.
- **RETURN**: Enters the typed information into the cell
  - **Note**: You must enter all of a player's information before you can move to change to a different player
- **F1**: Edit player entry screen
  - **Note**: You can use this after a game is over to return to the player entry screen 
- **F2**: Configure game parameters (Change Network Address Here)
- **F5**: Start the game
- **F7**: Create a new game (Not Implemented for this Project, can be added in a future iteration if wanted)
- **F12**: Clear the current game setup

## Players Needed To Start the Game
- Our code requires the game to have one player on each team to run the game. So, make sure that there is at least one player on each team to avoid errors.
- This can be changed in the future, we felt this worked best for standard games.

## Features
- Query and insert player details into a PostgreSQL database
- Interactive UI with a team selection system
- Gradient backgrounds and button-based navigation
- Error handling for database operations
- Displays Codename of player on the player entry screen after entering information
- Error handling for incorrect network addresses
- Overrides and deletes player information in the application when you enter new information in the same cell
- You can start a 6 minute game
- The game has a 30 seconds countdown before starting
- The game will start some background audio during the 30 second countdown and will continue until the game ends
- Players that hit the opposing team's base will receive a styleized letter B next to their name on the leaderboard for the rest of the game
- The highest scoring team will have their score flashing during the game.

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

