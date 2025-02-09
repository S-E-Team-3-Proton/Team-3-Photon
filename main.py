from python_db import PDB

def main():
    db = PDB()

    if db.connect():
        print("works!")
    else:
        print("NO")

    try:
        hold1 = db.get_player(1)
        if hold1:
            if hold1:
                print(f"found player: {hold1['codename']}")

                if db.set_EquipID(1, 69):
                    print("Assigned Equipment")
                    hID = db.get_EquipID(1)
                    print(f"Player e_id: {hID}")

        elif db.add_player(1,"Guy"):
            print("added player")

            hold1 = db.get_player(1)
            if hold1:
                print(f"found player: {hold1['codename']}")

                if db.set_EquipID(1, 69):
                    print("Assigned Equipment")
                    hID = db.get_EquipID(1)
                    print(f"Player e_id: {hID}")
            


        playersAndIDs = db.assigned_IDs()
        print(f"All info: {playersAndIDs}")

    finally:
        db.disconnect()

            

if __name__ == "__main__":
    main()
