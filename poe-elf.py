#----------------------------------------------------------------------------
#   poe-elf.py
#----------------------------------------------------------------------------
# Created By  : Connor Poland
# Created Date: 2022-06-22
# version ='0.0'
# ---------------------------------------------------------------------------
#   Path of Exile - Economy-Linked Loot Filter
# ---------------------------------------------------------------------------
#   
#   Usage - poe-elf.py
#
# ---------------------------------------------------------------------------
#   Example - python poe-elf.py
# ---------------------------------------------------------------------------
import sys
import time
import configparser
import capture_poeninja as CAPTURE
import ninja_indexGen as INDEX
import rand_indexGen as RAND_INDEX
import filterGen as GENERATE

#GLOBAL
leagueName = "Sentinel"
dumpDirPath = "./tmp_poe_ninja"
filterOutputPath = "./ELF.filter"
marketIndexPath = "./marketIndex.xml"
filterConfigPath = "./filterConfigs.xml"
refreshInterval = 1
randomValue = 0
refreshNotify = 1

configPath = "./elf.config"

def poe_elf():
    while(1):
        starttime = time.time() 
        CAPTURE.capture_poeninja(leagueName, dumpDirPath)
        if(randomValue):
            RAND_INDEX.indexGen(marketIndexPath, dumpDirPath)
        else:
            INDEX.indexGen(marketIndexPath, dumpDirPath)
        GENERATE.filterGen(filterOutputPath, marketIndexPath, filterConfigPath)
        #Filter done!
        if(refreshNotify):
            print("\a")
        if(refreshInterval > 0):
            endtime = time.time()
            sleeptime = (starttime+(refreshInterval*60)) - endtime
            if(sleeptime > 0):
                time.sleep(sleeptime)
        else:
            exit()

if __name__ == "__main__":
    #Load GLOBAL defaults (implicit)
    #Load config defaults (from ./elf.config)
    config = configparser.ConfigParser()
    config.read(configPath)
    if("POE" in config):
        if("leagueName" in config["LOCAL"]):
            leagueName = config["LOCAL"].get("leagueName")
        if("filterOutputPath" in config["LOCAL"]):
            filterOutputPath = config["LOCAL"].get("filterOutputPath")   
    if("LOCAL" in config):
        if("dumpDirPath" in config["LOCAL"]):
            dumpDirPath = config["LOCAL"].get("dumpDirPath")
        if("marketIndexPath" in config["LOCAL"]):
            marketIndexPath = config["LOCAL"].get("marketIndexPath")
        if("filterConfigPath" in config["LOCAL"]):
            filterConfigPath = config["LOCAL"].get("filterConfigPath")
        if("refreshInterval" in config["LOCAL"]):
            refreshInterval = config["LOCAL"].getint("refreshInterval")
        if("refreshNotify" in config["LOCAL"]):
            refreshNotify = config["LOCAL"].getboolean("refreshNotify")
    if("DEBUG" in config):
        if("randomValue" in config["DEBUG"]):
            randomValue = config["DEBUG"].getboolean("randomValue")
    #Load any command line args - TODO
    poe_elf()