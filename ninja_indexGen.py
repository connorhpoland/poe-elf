#----------------------------------------------------------------------------
#   ninja_indexGen.py
#----------------------------------------------------------------------------
# Created By  : Connor Poland
# Created Date: 2022-06-06
version = "0.0"
# ---------------------------------------------------------------------------
#   Path of Exile - Economy-Linked Loot Filter
# ---------------------------------------------------------------------------
#   
#   Usage - ninja_indexGen.py marketIndex.xml dumpDir 
#       marketIndex.xml - Path to the local index file to be created
#       dumpDir - Path to the directory that contains all poe.ninja JSON files to be indexed 
#
# ---------------------------------------------------------------------------
#   Example - python ninja_indexGen.py ./marketIndex.xml ./poe_ninja_2022_06_07
# ---------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime
import logging

USAGE = "\n   USAGE - ninja_indexGen.py marketIndex.xml dumpDir\n\
        marketIndex.xml - Path to the local index file to be created\n\
        dumpDir - Path to the directory that contains all poe.ninja JSON files to be indexed"

#GLOBAL
marketIndexPath = "./marketIndex.xml"
dumpDirPath = "./tmp_poe_ninja"
_log = logging.getLogger(__name__)

def getVersion():
    return version

#----- Common JSON Utils -----
def extractJSON(json_file_name):
    try:
        file_handle = open(json_file_name)
    except:
        _log.error("JSON file "+json_file_name+" cannot be openned")
        return 0
        
    try:
        json_data = json.load(file_handle)
    except:
        _log.error("JSON file "+json_file_name+" not a valid JSON documenmt")
        file_handle.close()
        return 0
    
    file_handle.close()
    return json_data

#----- marketIndex.xml Utils -----
def dictSetIfGreater(myDict, key, newValue):
    if(key not in myDict or myDict[key] < newValue):
        myDict[key] = newValue

#Items of class Currency have a name and value 
def addXMLItemCurrency(parent, name, value):
    #QUIRK There are some items in poe.ninjas data set that no longer exist in-game and may cause problems during filter creation
    if(name == "Maven's Orb" or name == "Silver Coin"):
        return
    newItem = ET.SubElement(parent, "item", name=name)
    ET.SubElement(newItem, "chaosValue").text = value
    return

#Items of class Unique have a basename, value, replica, links, and jewels
def addXMLItemUnique(parent, basename, value, replica, links):
    newItem = ET.SubElement(parent, "item", name=basename)
    ET.SubElement(newItem, "replica").text = str(replica)
    ET.SubElement(newItem, "links").text = str(links)
    ET.SubElement(newItem, "chaosValue").text = value
    return
    
#Items of class Gem have a name, value, level, quality, and corrupted
def addXMLItemGem(parent, name, value, level, quality, corrupted):
    qualityType = "Normal"
    if(name.startswith("Anomalous")):
        qualityType = "Anomalous"
        name = name[len("Anomalous "):]
    elif(name.startswith("Divergent")):
        qualityType = "Divergent"
        name = name[len("Divergent "):]
    elif(name.startswith("Phantasmal")):
        qualityType = "Phantasmal"
        name = name[len("Phantasmal "):]

    newItem = ET.SubElement(parent, "item", name=name)
    ET.SubElement(newItem, "qualityType").text = qualityType
    ET.SubElement(newItem, "level").text = level
    ET.SubElement(newItem, "quality").text = quality
    if(corrupted):
        ET.SubElement(newItem, "corrupted").text = "1"
    else:
        ET.SubElement(newItem, "corrupted").text = "0"
    ET.SubElement(newItem, "chaosValue").text = value
    return
    
#Items of class Base have a name, value, ilvl, and some number of 6 influences
def addXMLItemBase(parent, name, value, ilvl, shaper, elder, crusader, hunter, redeemer, warlord):
    newItem = ET.SubElement(parent, "item", name=name)
    ET.SubElement(newItem, "shaper").text = str(shaper)
    ET.SubElement(newItem, "elder").text = str(elder)
    ET.SubElement(newItem, "crusader").text = str(crusader)
    ET.SubElement(newItem, "hunter").text = str(hunter)
    ET.SubElement(newItem, "redeemer").text = str(redeemer)
    ET.SubElement(newItem, "warlord").text = str(warlord)
    ET.SubElement(newItem, "ilvl").text = str(ilvl)
    ET.SubElement(newItem, "chaosValue").text = value
    return
    
#Items of class Base have a name, value, ilvl, number of passives and an enchantment
def addXMLItemCluster(parent, name, value, ilvl, passives, enchantment):
    newItem = ET.SubElement(parent, "item", name=name)
    ET.SubElement(newItem, "passives").text = passives
    ET.SubElement(newItem, "enchantment").text = enchantment
    ET.SubElement(newItem, "ilvl").text = str(ilvl)
    ET.SubElement(newItem, "chaosValue").text = value
    return

#Class Currency (Currency.json, Artifact.json, Oil.json, DeliriumOrb.json, Fossil.json, Essence.json, Vial.json)
def addXMLClassCurrency(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Currency")

    #Parse through JSON data
    json_files_currency = {"/Currency.json"}
    json_files_item = {"/Artifact.json", "/Oil.json", "/DeliriumOrb.json", "/Fossil.json", "/Essence.json", "/Vial.json"}
    #QUIRK The Chaos Orb is not valued by poe.ninja - it's value it inherently known (1.00 Choas Orbs)
    addXMLItemCurrency(newClass, "Chaos Orb", "1.00")
    for file_name in json_files_currency:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["currencyTypeName"], str(item["chaosEquivalent"]))
        else:
            return 1 #ERROR - missing filter data
    for file_name in json_files_item:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["name"], str(item["chaosValue"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Map Fragments (Fragment.json, Scarab.json)  
def addXMLClassFragment(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Map Fragments")

    #Parse through JSON data
    json_files_currency = {"/Fragment.json"}
    json_files_item = {"/Scarab.json"}
    for file_name in json_files_currency:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["currencyTypeName"], str(item["chaosEquivalent"]))
        else:
            return 1 #ERROR - missing filter data
    for file_name in json_files_item:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["name"], str(item["chaosValue"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Divination (DivinationCard.json)
def addXMLClassDivination(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Divination")

    #Parse through JSON data
    json_files = {"/DivinationCard.json"}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["name"], str(item["chaosValue"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Incubators (Incubator.json)
def addXMLClassIncubator(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Incubator")

    #Parse through JSON data
    json_files = {"/Incubator.json"}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["name"], str(item["chaosValue"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Uniques (UniqueWeapon.json, UniqueArmour.json, UniqueAccessory.json, UniqueFlask.json, UniqueJewel.json, UniqueMap.json)
def addXMLClassUnqiue(parent, _dumpDirPath):
    #This class needs to be handled differently - Multiple uniques can have the same base and drastically different values
    #Loot Filters will not be able to identify the unqiue, so we assign a value to a base based on its highest value unique
    
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Unique")

    #Parse through JSON data
    json_files = {"/UniqueWeapon.json", "/UniqueArmour.json", "/UniqueAccessory.json", "/UniqueFlask.json", "/UniqueJewel.json", "/UniqueMap.json"}
    replica_dict = {}
    normal_dict = {}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                if(item["name"].startswith("Replica")):
                    if (not "links" in item):
                        dictSetIfGreater(replica_dict, item["baseType"], item["chaosValue"])
                    elif(item["links"] == 6):
                        dictSetIfGreater(replica_dict, "6L_"+item["baseType"], item["chaosValue"])
                    elif(item["links"] == 5):
                        dictSetIfGreater(replica_dict, "5L_"+item["baseType"], item["chaosValue"])
                else:
                    if (not "links" in item):
                        dictSetIfGreater(normal_dict, item["baseType"], item["chaosValue"])
                    elif(item["links"] == 6):
                        dictSetIfGreater(normal_dict, "6L_"+item["baseType"], item["chaosValue"])
                    elif(item["links"] == 5):
                        dictSetIfGreater(normal_dict, "5L_"+item["baseType"], item["chaosValue"])
        else:
            return 1 #ERROR - missing filter data
    for baseType in replica_dict:
        temp_links = 0
        if(baseType.startswith("6L_")):
            addXMLItemUnique(newClass, baseType[3:], str(replica_dict[baseType]), 1, 6)
        elif(baseType.startswith("5L_")):
            addXMLItemUnique(newClass, baseType[3:], str(replica_dict[baseType]), 1, 5)
        else:
            addXMLItemUnique(newClass, baseType, str(replica_dict[baseType]), 1, 0)
    for baseType in normal_dict:
        if(baseType.startswith("6L_")):
            addXMLItemUnique(newClass, baseType[3:], str(normal_dict[baseType]), 0, 6)
        elif(baseType.startswith("5L_")):
            addXMLItemUnique(newClass, baseType[3:], str(normal_dict[baseType]), 0, 5)
        else:
            addXMLItemUnique(newClass, baseType, str(normal_dict[baseType]), 0, 0)
    return 0

#Gems (SkillGem.json)
def addXMLClassGem(parent, _dumpDirPath):
    #The SkillGem.json file will have an variant attribute that encodes the level, quality, and corruption
    #variant can end with a c to encode corruption
    #variant may have one integer (which encodes level)
    #variant may have 2 integers seperated by / (which encodes level/quality)
    
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Gems")

    #Parse through JSON data
    json_files = {"/SkillGem.json"}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                b_corrupted = item["variant"].endswith("c")
                if(b_corrupted):
                    parse_variant = item["variant"][:-1].split("/")
                else:
                    parse_variant = item["variant"].split("/")
                if(len(parse_variant) == 1):
                    #No Quality
                    if(b_corrupted):
                        addXMLItemGem(newClass, item["name"], str(item["chaosValue"]), parse_variant[0], "0", b_corrupted)
                    else:
                        addXMLItemGem(newClass, item["name"], str(item["chaosValue"]), parse_variant[0], "0", b_corrupted)
                else:
                    #Non-0 Quality
                    addXMLItemGem(newClass, item["name"], str(item["chaosValue"]), parse_variant[0], parse_variant[1], b_corrupted)
        else:
            return 1 #ERROR - missing filter data
    return 0

#BaseTypes (BaseType.json, Sentinel.json, Invitation.json)
def addXMLClassBase(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Bases")

    #Parse through JSON data
    json_files_type = {"/BaseType.json"}
    json_files_other = {"/Sentinel.json", "/Invitation.json"}
    for file_name in json_files_type:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                b_shaper = 0
                b_elder = 0
                b_crusader = 0
                b_hunter = 0
                b_redeemer = 0
                b_warlord = 0
                if("variant" in item):
                    parse_variant = item["variant"].split("/")
                    for influence in parse_variant:
                        if(influence == "Shaper"):
                            b_shaper = 1
                        elif(influence == "Elder"):
                            b_elder = 1
                        elif(influence == "Crusader"):
                            b_crusader = 1
                        elif(influence == "Hunter"):
                            b_hunter = 1
                        elif(influence == "Redeemer"):
                            b_redeemer = 1
                        elif(influence == "Warlord"):
                            b_warlord = 1
                addXMLItemBase(newClass, item["baseType"], str(item["chaosValue"]), item["levelRequired"], b_shaper, b_elder, b_crusader, b_hunter, b_redeemer, b_warlord)
        else:
            return 1 #ERROR - missing filter data
    for file_name in json_files_other:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemBase(newClass, item["name"], str(item["chaosValue"]), 0, 0, 0, 0, 0, 0, 0)
        else:
            return 1 #ERROR - missing filter data
    return 0

#Cluster Jewels (ClusterJewel.json)
def addXMLClassCluster(parent, _dumpDirPath):
    #Cluster jewel variant contains the string "x passives"
    #Cluster jewel name contains the full enchantment text - we need to parse this to the reduced Loot Filter text
    def parseClusterEnchantment(clusterJewelSize, fullEnchantmentText):
        if(clusterJewelSize == "Large Cluster Jewel"):
            if(fullEnchantmentText.endswith("increased Attack Damage")):
                return "\"Attack Damage\""
            elif(fullEnchantmentText.endswith("increased Attack Damage while Dual Wielding")):
                return "\"Attack Damage while Dual Wielding\""
            elif(fullEnchantmentText.endswith("increased Attack Damage while holding a Shield")):
                return "\"Attack Damage while holding a Shield\""
            elif("Sword Attacks deal" in fullEnchantmentText and "Axe Attacks deal" in fullEnchantmentText):
                return "\"Axe and Sword Damage\""
            elif("increased Damage with Bows" in fullEnchantmentText):
                return "\"Bow Damage\""
            elif(fullEnchantmentText.endswith("increased Chaos Damage")):
                return "\"Chaos Damage\""
            elif(fullEnchantmentText.endswith("increased Cold Damage")):
                return "\"Cold Damage\""
            elif("Claw Attacks deal" in fullEnchantmentText and "Dagger Attacks deal" in fullEnchantmentText):
                return "\"Dagger and Claw Damage\""
            elif(fullEnchantmentText.endswith("increased Damage with Two Handed Weapons")):
                return "\"Damage with Two Handed Weapons\""
            elif(fullEnchantmentText.endswith("increased Elemental Damage")):
                return "\"Elemental Damage\""
            elif(fullEnchantmentText.endswith("increased Fire Damage")):
                return "\"Fire Damage\""
            elif(fullEnchantmentText.endswith("increased Lightning Damage")):
                return "\"Lightning Damage\""
            elif("Staff Attacks deal" in fullEnchantmentText and "Mace or Scepter Attacks deal" in fullEnchantmentText):
                return "\"Mace and Staff Damage\""
            elif("Minions deal" in fullEnchantmentText):
                return "\"Minion Damage\""
            elif(fullEnchantmentText.endswith("increased Physical Damage")):
                return "\"Physical Damage\""
            elif(fullEnchantmentText.endswith("increased Spell Damage")):
                return "\"Spell Damage\""
            elif("Wand Attacks deal" in fullEnchantmentText):
                return "\"Wand Damage\""
        elif(clusterJewelSize == "Medium Cluster Jewel"):
            if(fullEnchantmentText.endswith("increased Area Damage")):
                return "\"Area Damage\""
            elif(fullEnchantmentText.endswith("increased effect of Non-Curse Auras from your Skills")):
                return "\"Aura Effect\""    
            elif(fullEnchantmentText.endswith("increased Brand Damage")):
                return "\"Brand Damage\""
            elif("Channelling Skills deal" in fullEnchantmentText):
                return "\"Channelling Skill Damage\""
            elif(fullEnchantmentText.endswith("increased Chaos Damage over Time")):
                return "\"Chaos Damage over Time\""
            elif(fullEnchantmentText.endswith("increased Cold Damage over Time")):
                return "\"Cold Damage over Time\""
            elif(fullEnchantmentText.endswith("increased Critical Strike Chance")):
                return "\"Critical Chance\""
            elif(fullEnchantmentText.endswith("increased Effect of your Curses")):
                return "\"Curse Effect\""
            elif(fullEnchantmentText.endswith("increased Damage over Time")):
                return "\"Damage over Time\""
            elif(fullEnchantmentText.endswith("increased Damage while affected by a Herald")):
                return "\"Damage while you have a Herald\""
            elif(fullEnchantmentText.endswith("increased Effect of Non-Damaging Ailments")):
                return "\"Effect of Non-Damaging Ailments\""
            elif("Exerted Attacks deal" in fullEnchantmentText):
                return "\"Exerted Attack Damage\""
            elif(fullEnchantmentText.endswith("increased Fire Damage over Time")):
                return "\"Fire Damage over Time\""
            elif(fullEnchantmentText.endswith("increased Flask Effect Duration")):
                return "\"Flask Duration\""
            elif("Life Recovery from Flasks" in fullEnchantmentText and "Mana Recovery from Flasks" in fullEnchantmentText):
                return "\"Life and Mana recovery from Flasks\""
            elif(fullEnchantmentText.endswith("increased Damage while you are affected by a Herald")):
                return "\"Minion Damage while you have a Herald\""
            elif("Minions have" in fullEnchantmentText and "increased maximum Life" in fullEnchantmentText):
                return "\"Minion Life\""
            elif(fullEnchantmentText.endswith("increased Physical Damage over Time")):
                return "\"Physical Damage over Time\""
            elif(fullEnchantmentText.endswith("increased Projectile Damage")):
                return "\"Projectile Damage\""
            elif(fullEnchantmentText.endswith("increased Totem Damage")):
                return "\"Totem Damage\""
            elif("increased Trap Damage" in fullEnchantmentText and "increased Mine Damage" in fullEnchantmentText):
                return "\"Trap and Mine Damage\""
        else:
            if(fullEnchantmentText.endswith("increased Armour")):
                return "\"Armour\""
            elif(fullEnchantmentText.endswith("Chance to Block Attack Damage")):
                return "\"Chance to Block Attack Damage\""
            elif(fullEnchantmentText.endswith("Chance to Block Spell Damage")):
                return "\"Chance to Block Spell Damage\""
            elif(fullEnchantmentText.endswith("chance to Suppress Spell Damage")):
                return "\"Suppress\""
            elif(fullEnchantmentText.endswith("to Chaos Resistance")):
                return "\"Chaos Resistance\""
            elif(fullEnchantmentText.endswith("to Cold Resistance")):
                return "\"Cold Resistance\""
            elif(fullEnchantmentText.endswith("increased Effect of your Curses")):
                return "\"Curse Effect\""
            elif(fullEnchantmentText.endswith("increased maximum Energy Shield")):
                return "\"Energy Shield\""
            elif(fullEnchantmentText.endswith("increased Evasion Rating")):
                return "\"Evasion\""
            elif(fullEnchantmentText.endswith("to Fire Resistance")):
                return "\"Fire Resistance\""
            elif(fullEnchantmentText.endswith("increased maximum Life")):
                return "\"Life\""
            elif(fullEnchantmentText.endswith("to Lightning Resistance")):
                return "\"Lightning Resistance\""
            elif(fullEnchantmentText.endswith("increased maximum Mana")):
                return "\"Mana\""
            elif(fullEnchantmentText.endswith("increased Mana Reservation Efficiency of Skills")):
                return "\"Reservation Efficiency\""
        return fullEnchantmentText

    #Create XML class
    newClass = ET.SubElement(parent, "class", name="ClusterJewels")

    #Parse through JSON data
    json_files = {"/ClusterJewel.json"}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                parse_variant = item["variant"].split(" ")
                addXMLItemCluster(newClass, item["baseType"], str(item["chaosValue"]), item["levelRequired"], parse_variant[0], parseClusterEnchantment(item["baseType"], item["name"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Delve Stackable Socketable Currency (Resonator.json)
def addXMLClassResonator(parent, _dumpDirPath):
    #Create XML class
    newClass = ET.SubElement(parent, "class", name="Delve Stackable Socketable Currency")

    #Parse through JSON data
    json_files={"/Resonator.json"}
    for file_name in json_files:
        json_data = extractJSON(_dumpDirPath+file_name)
        if(json_data != 0):
            for item in json_data["lines"]:
                addXMLItemCurrency(newClass, item["name"], str(item["chaosValue"]))
        else:
            return 1 #ERROR - missing filter data
    return 0

#Ignored (Beast.json, BlightedMap.json, BlightRavagedMap.json, HelmetEnchant.json, Map.json)
def addXMLClassEtc(parent, _dumpDirPath):
    return 0

def indexGen(_marketIndexPath, _dumpDirPath):
    #Start the marketIndex.xml tree with the root structure <snapshot>
    marketSnapshot = ET.Element("snapshot", name="ninja_indexGen.py Market Index")

    #<snapshot> contains a few meta fields...
    #<version> contains the marketIndex.xml structure version
    ET.SubElement(marketSnapshot, "version").text="0.0"
    #<date> contains the current time and date d/m/y H:M:S
    now = datetime.now()
    dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
    ET.SubElement(marketSnapshot, "date").text=dt_str

    #Generate each item class XML tree under marketSnapshot
    #Currency
    if(addXMLClassCurrency(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Currency, cannot generate index")
        return 1 #ERROR
    #Map Fragments
    if(addXMLClassFragment(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Fragment, cannot generate index")
        return 1 #ERROR
    #Divination
    if(addXMLClassDivination(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Divination, cannot generate index")
        return 1 #ERROR
    #Incubators
    if(addXMLClassIncubator(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Incubator, cannot generate index")
        return 1 #ERROR
    #Uniques
    if(addXMLClassUnqiue(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Unique, cannot generate index")
        return 1 #ERROR
    #Gems
    if(addXMLClassGem(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Gem, cannot generate index")
        return 1 #ERROR
    #BaseTypes
    if(addXMLClassBase(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class BaseType, cannot generate index")
        return 1 #ERROR
    #Cluster Jewels
    if(addXMLClassCluster(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Cluster, cannot generate index")
        return 1 #ERROR
    #Delve Stackable Socketable Currency
    if(addXMLClassResonator(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Resonator, cannot generate index")
        return 1 #ERROR
    #Other/Etc
    if(addXMLClassEtc(marketSnapshot, _dumpDirPath)):
        _log.error("Missing poe.ninja data for class Other, cannot generate index")
        return 1 #ERROR

    #Dump the full XML tree to marketIndex.xml file path
    xmlTree = ET.ElementTree(marketSnapshot)
    try:
        xmlTree.write(_marketIndexPath, xml_declaration=True, encoding="utf-8")
    except:
        _log.error("Failed to write in-memory index XML to file "+_marketIndexPath)
        return 1 #EORROR
    
    return 0 #OK

if __name__ == "__main__":
    #Either specify no args (default) or both
    if(len(sys.argv) == 3):
        marketIndexPath = sys.argv[1]
        dumpDirPath = sys.argv[2]
    elif(len(sys.argv) != 1):
        print(USAGE)
        exit()

    indexGen(marketIndexPath, dumpDirPath)
    exit()