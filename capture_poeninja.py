#----------------------------------------------------------------------------
#   capture_poeninja.py
#----------------------------------------------------------------------------
# Created By  : Connor Poland
# Created Date: 2022-06-21
# version ='0.0'
# ---------------------------------------------------------------------------
#   Path of Exile - Economy-Linked Loot Filter
# ---------------------------------------------------------------------------
#   
#   Usage - capture_poeninja.py leagueName dumpDir 
#       leagueName - Name of the challenge league to be captured (Names with spaces should be quoted)
#       dumpDir - Path to the directory that will contain all requested poe.ninja JSON files
#
# ---------------------------------------------------------------------------
#   Example - capture_poeninja.py Sentinel ./tmp_poe_ninja
# ---------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sys
import requests

USAGE = "\n   USAGE - capture_poeninja.py leagueName dumpDir\n\
        leagueName - Name of the challenge league to be captured (Names with spaces should be quoted)\n\
        dumpDir - Path to the directory that will contain all requested poe.ninja JSON files"
        
#GLOBAL
leagueName = "Sentinel"
dumpDirPath = "./tmp_poe_ninja"

def requestToFile(requestResp, filename):
    #Open file associated with the request
    dumpFile = open(filename, "w", encoding="utf-8")
    if(dumpFile):
        dumpFile.write(requestResp.text)
        print(filename+" OK!")
        dumpFile.close()

currency_types = {"Currency", "Fragment"}
item_types = {"DivinationCard", "Artifact", "Oil", "Incubator", "UniqueWeapon", "UniqueArmour", 
    "UniqueAccessory", "UniqueFlask", "UniqueJewel", "SkillGem", "ClusterJewel", "Map", "BlightedMap", 
    "BlightRavagedMap", "UniqueMap", "Sentinel", "DeliriumOrb", "Invitation", "Scarab", "BaseType", "Fossil", 
    "Resonator", "HelmetEnchant", "Beast", "Essence", "Vial"}
def capture_poeninja(_leagueName, _dumpDirPath):
    for currency in currency_types:
        requestResp = requests.get("https://poe.ninja/api/data/currencyoverview?league="+_leagueName+"&type="+currency)
        if(requestResp.status_code == 200):
            requestToFile(requestResp, _dumpDirPath+"/"+currency+".json")
        else:
            print("Bad response for "+currency+" in league "+_leagueName)
    for item in item_types:
        requestResp = requests.get("https://poe.ninja/api/data/itemoverview?league="+_leagueName+"&type="+item)
        if(requestResp.status_code == 200):
            requestToFile(requestResp, _dumpDirPath+"/"+item+".json")
        else:
            print("Bad response for "+item+" in league "+_leagueName)

if __name__ == "__main__":
    #Either specify no args (default) or both
    if(len(sys.argv) == 3):
        leagueName = sys.argv[1]
        dumpDirPath = sys.argv[2]
    elif(len(sys.argv) != 1):
        print(USAGE)
        exit()

    capture_poeninja(leagueName, dumpDirPath)