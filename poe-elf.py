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
#   Usage - poe-elf.py generated.filter marketIndex.xml filterConfigs.xml
#       generated.filter - Path to the local filter file to be created
#       marketIndex.xml - Path to a local XML file containing a market index. (See: marketIndex.xml.help)
#       filterConfigs.xml - Path to a local XML file containing a configuartion preferences for the new filter. (See: filterConfigs.xml.help)
#
# ---------------------------------------------------------------------------
#   Example - python poe-elf.py ./ELF.filter ./marketIndex.xml ./filerConfigs.xml
# ---------------------------------------------------------------------------
import sys
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
refreshInterval = "3"
randomValue = "0"

def poe_elf():
    CAPTURE.capture_poeninja(leagueName, dumpDirPath)
    INDEX.indexGen(marketIndexPath, dumpDirPath)
    GENERATE.filterGen(filterOutputPath, marketIndexPath, filterConfigPath)

if __name__ == "__main__":
    poe_elf()