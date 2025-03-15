import pygame
from player import Player

def is_valid_ip(ip):
    try:
        import ipaddress
        ipaddress.ip_address(ip) 
        return True
    except ValueError:
        return False
    
def handle_event(event, game_state, app_client, app_server):
    if event.type == pygame.KEYDOWN:
        if game_state.active_view == "entry":
            if event.key == pygame.K_F12:  # Clear game
                game_state.red_team = [Player() for _ in range(15)]
                game_state.green_team = [Player() for _ in range(15)]
                game_state.current_index = 0
                game_state.active_input = "p_id"
                game_state.input_text = ""
                game_state.db.reset_EquipID()
            elif event.key == pygame.K_F5:  # Start game
                red_has_player = any(player.player_id for player in game_state.red_team)
                green_has_player = any(player.player_id for player in game_state.green_team)
                
                if not (red_has_player and green_has_player):
                    print("Each team needs at least 1 player to start the game.")
                    return
                
                allequiped, missing_equip = validate_equipIDS(game_state.red_team, game_state.green_team)

                if not allequiped:
                    for player_info in missing_equip:
                        print(f"{player_info} lacking equipment ID")
                    return
                
                game_state.gameStart(app_client)
            elif event.key == pygame.K_F2: # Switch to game parameters screen (change network address here)
                game_state.active_view = "parameters"
                game_state.previous_input = game_state.active_input
                game_state.active_input = "ip_address"
            else:
                handleInfo(event, game_state, app_client)
        elif game_state.active_view == "parameters":
            if event.key == pygame.K_F1:  # Change to edit game
                game_state.active_view = "entry"
                game_state.active_input = game_state.previous_input or "p_id"
                game_state.input_text = ''
            elif event.key == pygame.K_F5:  # Start game
                red_has_player = any(player.player_id for player in game_state.red_team)
                green_has_player = any(player.player_id for player in game_state.green_team)
                
                if not (red_has_player and green_has_player):
                    print("Each team needs at least 1 player to start the game.")
                    return
                
                allequiped, missing_equip = validate_equipIDS(game_state.red_team, game_state.green_team)

                if not allequiped:
                    for player_info in missing_equip:
                        print(f"{player_info} lacking equipment ID")
                    return
                
                game_state.gameStart(app_client)
            elif event.key == pygame.K_RETURN:  # Start network address entry
                if is_valid_ip(game_state.input_text.strip()):
                    new_ip_address = game_state.input_text.strip()
                    app_client.set_network_address(new_ip_address)
                    app_server.set_network_address(new_ip_address)
                    print(f"Changed Network address to {new_ip_address}")
                    game_state.active_input = 'entry'
                    game_state.active_input = game_state.previous_input or 'p_id'
                else:
                    print("⚠️ Invalid Network Address!")
                game_state.input_text = ""  # Clear input box
            elif event.key == pygame.K_BACKSPACE:
                game_state.input_text = game_state.input_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                game_state.active_view ='entry'
                game_state.active_input = game_state.previous_input or 'p_id'
                game_state.input_text= ''
            else:
                try:
                    char = event.unicode
                    if char.isprintable():
                        game_state.input_text += char
                except:
                    pass
        elif game_state.active_view == "game" and game_state.gameOver:
            if event.key == pygame.K_F1:
                game_state.active_view = "entry"
                game_state.running = False
                game_state.gameOver = False
                game_state.active_input = "p_id"
        
def handleInfo(event, game_state, app_client):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        # print("ENTER key detected")
        if game_state.active_input == "p_id" and game_state.input_text:
            player_id = game_state.input_text.strip()
            # print(f"Setting player ID directly to: {player_id}")

            if player_id.isdigit():
                # Get the current team's player array
                team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
                other_team = game_state.green_team if game_state.current_team == "red" else game_state.red_team
                
                player_exist = False
                for i, player in enumerate(team):
                    if player.player_id == player_id and i!= game_state.current_index:
                        player_exist = True
                        break

                for player in other_team:
                    if player.player_id == player_id:
                        player_exist = True
                        break

                if player_exist:
                    print(f"Player ID {player_id} already exists!")
                    game_state.input_text = ''
                    return

                team[game_state.current_index].player_id = player_id
                
                # Query database for existing codename
                if player_id.isdigit():
                    codename = game_state.query_codename(player_id)
                    if codename:
                        print(f"Found codename in database: {codename}")
                        team[game_state.current_index].codename = codename
            else:
                print("Invalid Player ID!")
                game_state.input_text = ''
                return
            
            # Move to equipment ID field
            game_state.active_input = "e_id"
            game_state.input_text = ""
            return
        elif game_state.active_input == "e_id" and game_state.input_text:
            equipment_id = game_state.input_text.strip()
            # print(f"Setting equipment ID directly to: {equipment_id}")
            
            if equipment_id.isdigit():  
                team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
                other_team = game_state.green_team if game_state.current_team == "red" else game_state.red_team
                
                equipment_exist = False
                for i, player in enumerate(team):
                    if player.equipment_id == int(equipment_id) and i!= game_state.current_index:
                        equipment_exist = True
                        break

                for player in other_team:
                    if player.equipment_id == int(equipment_id):
                        equipment_exist = True
                        break

                if equipment_exist:
                    print(f"Equipment ID {equipment_id} already exists!")
                    game_state.input_text = ''
                    return

                # Store the equipment ID
                team[game_state.current_index].equipment_id = int(equipment_id)
                
                # Try to send to client
                try:
                    app_client.send_message(equipment_id)
                    print(f"Sent equipment ID {equipment_id} to client")
                except Exception as e:
                    print(f"Warning: Could not send equipment ID: {e}")
            else:
                print("Invalid Equipment ID!")
                game_state.input_text = ''
                return
            
            # Move to name field
            if team[game_state.current_index].codename:
                # If codename exists, move to next player
                game_state.current_index = (game_state.current_index + 1) % 15
                game_state.active_input = "p_id"
            else:
                # Otherwise, move to name field
                game_state.active_input = "name"
            game_state.input_text = ""
            return
        elif game_state.active_input == "name" and game_state.input_text:
            codename = game_state.input_text.strip()
            # print(f"Setting codename directly to: {codename}")
            
            team = game_state.red_team if game_state.current_team == "red" else game_state.green_team
            other_team = game_state.green_team if game_state.current_team == "red" else game_state.red_team
            
            codename_exist = False
            for i, player in enumerate(team):
                if player.codename == codename and i!= game_state.current_index:
                    codename_exist = True
                    break

            for player in other_team:
                if player.codename == codename:
                    codename_exist = True
                    break

            if codename_exist:
                print(f"Codename {codename} already exists!")
                game_state.input_text = ''
                return
            
            player_id = team[game_state.current_index].player_id
            
            # Store the codename
            team[game_state.current_index].codename = codename
            
            if player_id and player_id.isdigit():
                player_id_int = int(player_id)
                try:
                    db = game_state.db
                    if db and hasattr(db, 'update_player'):
                        result = db.update_player(player_id_int, codename)
                        if result:
                            print(f"Successfully updated player {player_id} with codename {codename}")
                        else:
                            print(f"Failed to update player {player_id} in database")
                    else:
                        game_state.db.add_player(player_id_int, codename)
                        print(f"Added player {player_id} with codename {codename} to database")
                except Exception as e:
                    print("Warning: Could not update database")
            
            # Move to next player
            game_state.current_index = (game_state.current_index + 1) % 15
            game_state.active_input = "p_id"
            game_state.input_text = ""
            return


    selectedTeam = game_state.red_team if game_state.current_team == "red" else game_state.green_team
    otherTeam = game_state.green_team if game_state.current_team == "green" else game_state.red_team

    if event.key == pygame.K_DOWN:
        game_state.current_index = (game_state.current_index + 1) % 15
    elif event.key == pygame.K_UP:
        game_state.current_index = (game_state.current_index - 1) % 15
    elif event.key == pygame.K_TAB:
        game_state.current_team = "green" if game_state.current_team == "red" else "red"
    elif event.key == pygame.K_BACKSPACE:
        game_state.input_text = game_state.input_text[:-1]
    else:
        try:
            char = event.unicode
            if char.isprintable():
                game_state.input_text += char
        except:
            pass

def validate_equipIDS(red_team, green_team):
    allValid = True
    missing = []

    for tname, team in [("Red", red_team), ("Green", green_team)]:
        for i, player in enumerate(team):
            if player.player_id and not player.equipment_id:
                allValid = False
                missing.append(f"{tname} PLayer #{i+1}: {player.player_id}")
    
    return allValid, missing
