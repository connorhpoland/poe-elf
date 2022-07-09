#----------------------------------------------------------------------------
#   poe-elf.py
#----------------------------------------------------------------------------
# Created By  : Connor Poland
# Created Date: 2022-07-09
version = "1.0"
# ---------------------------------------------------------------------------
#   Path of Exile - Economy-Linked Loot Filter
# ---------------------------------------------------------------------------
#   
#   Usage - poe-elf.py
#
# ---------------------------------------------------------------------------
#   Example - python poe-elf.py
# ---------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import sys
import time
import configparser
import logging
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
loggingLevel = 40 #ERROR
loggingPath = 0
filterRetryCount = 3

configPath = "./elf.config"

def getVersion():
    return version

def poe_elf():
    nRetry = 0
    while(1):
        if(nRetry == 0):
            starttime = time.time()
            logging.info("Starting to generate new filter")
        elif (nRetry > filterRetryCount):
            logging.error("Failed to generate filter after "+str(filterRetryCount)+" attempts. Review logs and configurations.")
            return 1
        if(CAPTURE.capture_poeninja(leagueName, dumpDirPath)):
            nRetry += 1
            logging.error("Failed to capture poeninja data... Restarting filter generation")
            continue
        if(randomValue):
            if(RAND_INDEX.indexGen(marketIndexPath, dumpDirPath)):
                nRetry += 1
                logging.error("Failed to parse (random) economy data into index... Restarting filter generation")
                continue
        else:
            if(INDEX.indexGen(marketIndexPath, dumpDirPath)):
                nRetry += 1
                logging.error("Failed to parse economy data into index... Restarting filter generation")
                continue
        if(GENERATE.filterGen(filterOutputPath, marketIndexPath, filterConfigPath)):
            nRetry += 1
            logging.error("Failed to create filter from market index... Restarting filter generation")
            continue
        
        #Filter done!
        nRetry = 0
        logging.critical("New filter generated! "+filterOutputPath)
        if(refreshNotify):
            print("\a")
            
        if(refreshInterval > 0):
            endtime = time.time()
            sleeptime = (starttime+(refreshInterval*60)) - endtime
            if(sleeptime > 0):
                logging.info("Sleeping for "+str(sleeptime)+" seconds before generating another filter")
                time.sleep(sleeptime)
        else:
            return 0

if __name__ == "__main__":
    #Load GLOBAL defaults (implicit)
    
    #Load config defaults (from ./elf.config)
    config = configparser.ConfigParser()
    config.read(configPath)
    if("POE" in config):
        if("leagueName" in config["POE"]):
            leagueName = config["POE"].get("leagueName")
        if("filterOutputPath" in config["POE"]):
            filterOutputPath = config["POE"].get("filterOutputPath")
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
        if("loggingLevel" in config["DEBUG"]):
            loggingLevel = config["DEBUG"].getint("loggingLevel")
        if("loggingPath" in config["DEBUG"]):
            loggingPath = config["DEBUG"].get("loggingPath")
            
    #Load any command line args - TODO
    
    #Init logging module
    if(loggingPath != 0):
        logging.basicConfig(filename=loggingPath,level=loggingLevel)
    else:
        logging.basicConfig(level=loggingLevel)
        
    logging.critical("Path of Exile - Economy-Linked Loot Filter v"+getVersion())
    logging.info(CAPTURE.__name__+".py v"+CAPTURE.getVersion())
    logging.info(INDEX.__name__+".py v"+INDEX.getVersion())
    logging.info(RAND_INDEX.__name__+".py v"+RAND_INDEX.getVersion())
    logging.info(GENERATE.__name__+".py v"+GENERATE.getVersion())
        
    #Dump configs to logs
    logging.info("leagueName = "+leagueName)
    logging.info("dumpDirPath = "+dumpDirPath)
    logging.info("filterOutputPath = "+filterOutputPath)
    logging.info("marketIndexPath = "+marketIndexPath)
    logging.info("filterConfigPath = "+filterConfigPath)
    logging.info("refreshInterval = "+str(refreshInterval))
    logging.info("randomValue = "+str(randomValue))
    logging.info("refreshNotify = "+str(refreshNotify))
    logging.info("loggingLevel = "+logging.getLevelName(loggingLevel))
    if(loggingPath):
        logging.info("loggingPath = "+loggingPath)
    else:
        logging.info("logginPath = NONE (CMD)")
        
    try: 
        poe_elf()
        logging.critical("Shutting down poe-elf")
    except KeyboardInterrupt:
        logging.critical("Shutting down poe-elf (Interrupt Recv'd)")
    except:
        logging.critical("Shutting down poe-elf (Untrapped Exception)")
    exit()