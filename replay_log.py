import pickle

#sample code for retrieving stuff that was logged
#note: each file in the RunData is a separate run. it is split into steps, where each one contains
    # info about assets, tracks, and actions taken
    # it is in the format of a dictionary
    # ex: the key "asset" links to a list of the various assets, and so on

#note: files in RunData are named based off of which run they are in a sequence, and the current date

# Step#: {Step: #, Time: #, Score: #, Assets: [[asset 1 assetName, isHVU, health, [Position X,Y,Z], [LLe], [[weapon 1 weaponName, quantity, status] , [weapon 2 info]] ], [asset 2 info]],
# Tracks:  [[track 1 trackID, threatID, [LLE], [Position X,Y,Z], [Velocity X,Y,Z], [track 2]], actions: [{ action 1 Target: TrackID, Attacker: assetName, weapon: weaponName}, {action 2 info}]}

if __name__ == '__main__':
    filepath = "data/run1_0129" # example file name (change)
    with open(filepath, 'rb') as handle:
        data = pickle.load(handle)
        # print(data)hh
        # for i in data:
        #     print(data.get(i), "\n\n\n")
        #filtering examplesc
        # print(data.get(1)) #just the first step
        # print("\n\n\n\n")
    print(data.get(2).get("Assets")[1:]) #just the assets
    print("\n\n\n\n")

