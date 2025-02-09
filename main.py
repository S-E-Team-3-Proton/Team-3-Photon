from python_db import PDB

def main():
    db = PDB()

    if db.connect():
        print("works!")
    else:
        print("NO")

    vT = 1
    try:
        hold1 = db.get_player(vT)
        if hold1:
            if hold1:
                print(f"found player: {hold1['codename']}")

                if db.set_EquipID(vT, 69):
                    print("Assigned Equipment")
                    hID = db.get_EquipID(vT)
                    print(f"Player e_id: {hID}")

        elif db.add_player(vT,"Guy"):
            print("added player")

            hold1 = db.get_player(vT)
            if hold1:
                print(f"found player: {hold1['codename']}")

                if db.set_EquipID(vT, 69):
                    print("Assigned Equipment")
                    hID = db.get_EquipID(vT)
                    print(f"Player e_id: {hID}")

        playersAndIDs = db.assigned_IDs()
        print(f"All info: {playersAndIDs}")

    finally:
        db.disconnect()

            

if __name__ == "__main__":
    main()
