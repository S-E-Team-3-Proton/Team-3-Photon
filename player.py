class Player:
    def __init__(self, player_id="", codename="", equipment_id=None):
        self.player_id = player_id
        self.codename = codename 
        self.equipment_id = int(equipment_id) if equipment_id and equipment_id.isdigit() else 0
        self.score = 0
