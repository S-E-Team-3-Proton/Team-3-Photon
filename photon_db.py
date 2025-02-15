import psycopg2

class PDB:
    def __init__(self):
        self.connection = None
        self.pointer = None
        self.equipped_yes = {}

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="photon",
                user="student",
                password='student',
                host="127.0.0.1",
                port="5432"
            )
            self.pointer = self.connection.cursor()
            return True
        except:
            print("cant connect to Postgres")
            return False

    def disconnect(self):
        if self.pointer:
            self.pointer.close()
        if self.connection:
            self.connection.close()

    #use id to get info
    def get_player(self, p_id):
        try:
            #set pointer
            self.pointer.execute(
                "SELECT id, codename FROM players where id = %s",
                (p_id,)
            )
            #get from pointer
            res = self.pointer.fetchone()

            if res:
                return {
                    "id": res[0],
                    "codename": res[1],
                    "equip_id": self.equipped_yes.get(res[0], None)
                }
            return None
        except:
            print("Error getting player")
            return None

    def add_player(self, p_id, name):
        try:
            self.pointer.execute(
                "INSERT INTO players (id, codename) VALUES (%s,%s)",
                (p_id, name)
            )
            self.connection.commit()
            return True
        except:
            print("Error adding player")
            self.connection.rollback()
            return False

              
    def set_EquipID(self, p_id, e_id):
        if e_id in self.equipped_yes.values():
            return False
        
        self.equipped_yes[p_id] = e_id
        print(self.equipped_yes)
        return True
    
    def get_EquipID(self, p_id):
        return self.equipped_yes.get(p_id)

    def reset_EquipID(self):
        self.equipped_yes.clear()
    
    def remove_EquipID(self, p_id):
        del self.equipped_yes[int(p_id)]

    #return pla
    def assigned_IDs(self):
        plist = []
        for p_id, e_id in self.equipped_yes.items():
            pl = self.get_player(p_id)
            if pl:
                plist.append(pl)
        return plist
