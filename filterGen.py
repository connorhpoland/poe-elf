#----------------------------------------------------------------------------
#   filterGen.py
#----------------------------------------------------------------------------
# Created By  : Connor Poland
# Created Date: 2022-06-06
# version ='0.0'
# ---------------------------------------------------------------------------
#   Path of Exile - Economy-Linked Loot Filter
# ---------------------------------------------------------------------------
#   
#   Usage - filterGen.py generated.filter marketIndex.xml filterConfigs.xml
#       generated.filter - Path to the local filter file to be created
#       marketIndex.xml - Path to a local XML file containing a market index. (See: marketIndex.xml.help)
#       filterConfigs.xml - Path to a local XML file containing a configuartion preferences for the new filter. (See: filterConfigs.xml.help)
#
# ---------------------------------------------------------------------------
#   Example - python filterGen.py ./ELF.filter ./marketIndex.xml ./filerConfigs.xml
# ---------------------------------------------------------------------------
import sys
import xml.etree.ElementTree as ET

USAGE = "\n   USAGE - filterGen.py generated.filter marketIndex.xml filterConfigs.xml\n\
        generated.filter - Path to the local filter file to be created\n\
        marketIndex.xml - Path to a local XML file containing a market index (See: marketIndex.xml.help)\n\
        filterConfigs.xml - Path to a local XML file containing a configuartion preferences for the new filter. (See: filterConfigs.xml.help)"

#GLOBAL
filterOutputPath = "./ELF.filter"
marketIndexPath = "./marketIndex.xml"
filterConfigPath = "./filterConfigs.xml.help"

def clearTierData(tierNames, numTiers):
    for tier in range(numTiers):
        tierNames[tier] = ""
        
def addItemToTier(itemName, itemValue, tierNames, numTiers, valueTiers):
    for tier in range(numTiers):
        if(float(itemValue) >= valueTiers[tier]):
            tierNames[tier] +=" \""+itemName+"\""
            break

#Add a formatted block of tiered like-items to the filter file
def addSimpleFilterBlock(filterFile, className, tierNames, displayTiers, numTiers, extraFilterInfo):
    #Check to see that the whole isn't empty
    bEmpty = 1
    for tier in range(numTiers):
        if(tierNames[tier] != ""):
            bEmpty = 0
            break
    if (bEmpty):
        return
    #Annotate filter with Class
    filterFile.write("#CLASS "+className+"\n")
    for tier in range(numTiers):
        if(tierNames[tier] == ""):
            #No filter entry for empty tiers
            continue
        if(tier == numTiers-1):
            filterFile.write("Hide #TIER HIDE\n")
        else:
            filterFile.write("Show #"+"TIER "+str(tier)+"\n")
        if(extraFilterInfo):
            filterFile.write(extraFilterInfo)
        filterFile.write("BaseType "+tierNames[tier]+"\n")
        filterFile.write(displayTiers[tier]+"\n")
    clearTierData(tierNames, numTiers)

#Add a wildcard formatted hide-tier block to the filter file
def addHideFilterBlock(filterFile, displayTiers, numTiers):
    filterFile.write("Hide #WILDCARD HIDE - Match any not listed above\n")
    filterFile.write(displayTiers[numTiers-1]+"\n")

def main():
    #Filter Tiers, Meta - Ordered highest to lowest
    numTiers = 0
    valueTiers = {}
    displayTiers = {}
    
    #Load filterConfig to parse and setup filter tiers
    filterConfig = ET.parse(filterConfigPath).getroot()
    for valueTier in filterConfig.iter("tier"):
        valueTiers[numTiers] = float(valueTier.find("chaosValue").text)
        displayTiers[numTiers] = valueTier.find("display").text
        numTiers=numTiers+1
       
    #Open filter file for creation
    filterFile = open(filterOutputPath, "w")
       
    #Special Cases - Filter rules bellonging to a special case need to beed listed first so they dont get hidden
    for staticEntry in filterConfig.iter("static"):
        filterFile.write("#STATIC ENTRY "+staticEntry.get("name")+"\n")
        filterFile.write(staticEntry.find("display").text+"\n")
    
    #Clear and initialize the list of item names
    tierNames = {}
    clearTierData(tierNames, numTiers)
    
    #For each class in marketIndex populate a number of filter tiers based on filterConfig
    marketIndex = ET.parse(marketIndexPath).getroot()
    for itemClass in marketIndex.iter("class"):
        #Currency-type Class (Just filter by name)
        if(itemClass.get("name") == "Currency" or 
            itemClass.get("name") == "Map Fragments" or
            itemClass.get("name") == "Divination" or 
            itemClass.get("name") == "Incubator" or
            itemClass.get("name") == "Delve Stackable Socketable Currency"):
            for item in itemClass.iter("item"):
                #Determine which tier this item is in - then add it's name to that tiers name list
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name"), tierNames, displayTiers, numTiers, "Class \""+itemClass.get("name")+"\"\n")
                
        if(itemClass.get("name") == "Unique"):
            #Normal 6Ls
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "0" or item.find("links").text != "6"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" NORMAL 6 LINKS", tierNames, displayTiers, numTiers, "Rarity Unique\nLinkedSockets 6\n")
            #Replica 6Ls
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "1" or item.find("links").text != "6"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" REPLICA 6 LINKS", tierNames, displayTiers, numTiers, "Replica True\nRarity Unique\nLinkedSockets 6\n")
            #Normal 5Ls
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "0" or item.find("links").text != "5"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" NORMAL 5 LINKS", tierNames, displayTiers, numTiers, "Rarity Unique\nLinkedSockets 5\n")
            #Replica 5Ls
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "1" or item.find("links").text != "5"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" REPLICA 5 LINKS", tierNames, displayTiers, numTiers, "Replica True\nRarity Unique\nLinkedSockets 5\n")
            #Normal
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "0" or item.find("links").text != "0"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" NORMAL", tierNames, displayTiers, numTiers, "Rarity Unique\n")
            #Relica
            for item in itemClass.iter("item"):
                if(item.find("replica").text != "1" or item.find("links").text != "0"):
                    continue
                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
            addSimpleFilterBlock(filterFile, itemClass.get("name")+" REPLICA", tierNames, displayTiers, numTiers, "Replica True\nRarity Unique\n")
            
        if(itemClass.get("name") == "Gems"):
            #Corrupted
            for level in range (21, -1, -1):
                for quality in range (23, -1, -1):
                    for item in itemClass.iter("item"):
                        if(item.find("level").text == str(level) and item.find("quality").text == str(quality) and item.find("corrupted").text == "1"):
                            addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                    addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+str(level)+"/"+str(quality)+" Corrupted", tierNames, displayTiers, numTiers, "Class \"Gems\"\nCorrupted True\nGemLevel "+str(level)+"\nQuality "+str(quality)+"\n")
            #Un-Corrupted
            for level in range (20, -1, -1):
                for quality in range (20, -1, -1):
                    for item in itemClass.iter("item"):
                        if(item.find("level").text == str(level) and item.find("quality").text == str(quality) and item.find("corrupted").text == "1"):
                            addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                    addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+str(level)+"/"+str(quality), tierNames, displayTiers, numTiers, "Class \"Gems\"\nCorrupted False\nGemLevel "+str(level)+"\nQuality "+str(quality)+"\n")
            
        def isClusterJewel(itemName):
            if itemName.endswith("Cluster Jewel"):
                return 1
            return 0
        
        if(itemClass.get("name") == "ClusterJewels"):
            ilvls = {"84", "75", "68", "50", "1"}
            #Large Cluster Jewel
            #TODO We can tier out enchantments for ilvl/passive combos (not create a SimpleFilterBlock for each enchantment)
            large_passives = {"8", "9", "10", "11", "12"}
            large_enchantments = {"\"Attack Damage\"", "\"Attack Damage while Dual Wielding\"", "\"Attack Damage while holding a Shield\"", "\"Axe and Sword Damage\"", "\"Bow Damage\"",
                "\"Chaos Damage\"", "\"Cold Damage\"", "\"Dagger and Claw Damage\"", "\"Damage with Two Handed Weapons\"", "\"Elemental Damage\"", "\"Fire Damage\"", "\"Lightning Damage\"",
                "\"Mace and Staff Damage\"", "\"Minion Damage\"", "\"Physical Damage\"", "\"Spell Damage\"", "\"Wand Damage\""}
            for ilvl in ilvls:
                for passives in large_passives:
                    for enchantment in large_enchantments:
                        for item in itemClass.iter("item"):
                            if(item.get("name") == "Large Cluster Jewel" and item.find("ilvl").text == ilvl and item.find("passives").text == passives and item.find("enchantment").text == enchantment):
                                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                        addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+item.get("name")+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, 
                        "EnchantmentPassiveNum "+passives+"\nEnchantmentPassiveNode "+enchantment+"\nItemLevel >= "+ilvl+"\nRarity <= Rare\n")
            #Medium Cluster Jewel
            #TODO We can tier out enchantments for ilvl/passive combos (not create a SimpleFilterBlock for each enchantment)
            medium_passives = {"4", "5", "6"}
            medium_enchantments = {"\"Area Damage\"", "\"Aura Effect\"", "\"Brand Damage\"", "\"Channelling Skill Damage\"", "\"Chaos Damage over Time\"", "\"Cold Damage over Time\"", 
                "\"Critical Chance\"", "\"Curse Effect\"", "\"Damage over Time\"", "\"Damage while you have a Herald\"", "\"Effect of Non-Damaging Ailments\"", "\"Exerted Attack Damage\"", 
                "\"Fire Damage over Time\"", "\"Flask Duration\"", "\"Life and Mana recovery from Flasks\"", "\"Minion Damage while you have a Herald\"", "\"Minion Life\"", "\"Physical Damage over Time\"",
                "\"Projectile Damage\"", "\"Totem Damage\"", "\"Trap and Mine Damage\""}
            for ilvl in ilvls:
                for passives in medium_passives:
                    for enchantment in medium_enchantments:
                        for item in itemClass.iter("item"):
                            if(item.get("name") == "Medium Cluster Jewel" and item.find("ilvl").text == ilvl and item.find("passives").text == passives and item.find("enchantment").text == enchantment):
                                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                        addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+item.get("name")+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, 
                        "EnchantmentPassiveNum "+passives+"\nEnchantmentPassiveNode "+enchantment+"\nItemLevel >= "+ilvl+"\nRarity <= Rare\n")
            #Small Cluster Jewel
            #TODO We can tier out enchantments for ilvl/passive combos (not create a SimpleFilterBlock for each enchantment)
            small_passives = {"2", "3"}
            small_enchantments = {"\"Armour\"", "\"Chance to Block Attack Damage\"", "\"Chance to Block Spell Damage\"", "\"Suppress\"", "\"Chaos Resistance\"", "\"Cold Resistance\"", "\"Curse Effect\"",
            "\"Energy Shield\"", "\"Evasion\"", "\"Fire Resistance\"", "\"Life\"", "\"Lightning Resistance\"", "\"Mana\"", "\"Reservation Efficiency\""}
            for ilvl in ilvls:
                for passives in small_passives:
                    for enchantment in small_enchantments:
                        for item in itemClass.iter("item"):
                            if(item.get("name") == "Small Cluster Jewel" and item.find("ilvl").text == ilvl and item.find("passives").text == passives and item.find("enchantment").text == enchantment):
                                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                        addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+item.get("name")+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, 
                        "EnchantmentPassiveNum "+passives+"\nEnchantmentPassiveNode "+enchantment+"\nItemLevel >= "+ilvl+"\nRarity <= Rare\n")
            
        if(itemClass.get("name") == "Bases"):
            influences = {"shaper", "elder", "crusader", "hunter", "redeemer", "warlord"}
            ilvls = {"86", "85", "84", "83", "82"}
            def hasNumInfluences(item, num):
                influence_count = 0
                for influence in influences:
                    if(item.find(influence).text == "1"):
                        influence_count = influence_count+1
                if(influence_count != num):
                    return 0
                return 1
            #Double Influence 
            for first_influence in influences:
                for second_influence in influences:
                    if(first_influence == second_influence):
                        continue
                    for ilvl in ilvls:
                        for item in itemClass.iter("item"):
                            if(item.find(first_influence).text == "1" and item.find(second_influence).text == "1" and item.find("ilvl").text == ilvl and not isClusterJewel(item.get("name"))):
                                addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                        addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+first_influence+"/"+second_influence+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, 
                            "HasInfluence "+first_influence+"\nHasInfluence "+second_influence+"\nItemLevel >= "+ilvl+"\nRarity <= Rare\n")
            #Single Influence
            for influence in influences:
                for ilvl in ilvls:
                    for item in itemClass.iter("item"):
                        if(item.find(influence).text == "1" and hasNumInfluences(item, 1) and item.find("ilvl").text == ilvl and not isClusterJewel(item.get("name"))):
                            addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                    addSimpleFilterBlock(filterFile, itemClass.get("name")+" "+influence+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, "HasInfluence "+influence+"\nItemLevel >= "+ilvl+"\nRarity <= Rare\n")
            #Uninfluenced
            for ilvl in ilvls:
                for item in itemClass.iter("item"):
                    if(hasNumInfluences(item, 0) and item.find("ilvl").text == ilvl and not isClusterJewel(item.get("name"))):
                        addItemToTier(item.get("name"), item.find("chaosValue").text, tierNames, numTiers, valueTiers)
                addSimpleFilterBlock(filterFile, itemClass.get("name")+" ilvl "+ilvl+"+", tierNames, displayTiers, numTiers, "ItemLevel >= "+ilvl+"\nRarity <= Rare\n")
    
    #Add a Hide entry to hide any item that has not matched with a rule above
    addHideFilterBlock(filterFile, displayTiers, numTiers)
                
    filterFile.close()

if __name__ == "__main__":
    #Either specify no args (default) or both
    if(len(sys.argv) == 4):
        filterOutputPath = sys.argv[1]
        marketIndexPath = sys.argv[2]
        filterConfigPath = sys.argv[3]
    elif(len(sys.argv) != 1):
        print(USAGE)
        exit()
    main()