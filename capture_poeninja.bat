@echo off
:: Created By  : Connor Poland
:: Created Date: 2022-06-06
set version=0.0

:: This .bat script uses the CURL command line utility to capture a file set from the poe.ninja server
:: USAGE capture_poeninja.bat {leagueName} {dumpDir}
:: 		leagueName - Name of the challenge league to capture (ex. Sentinel, SentinelHC)
::		dumpDir - Path to dir to dump JSON files 

set currency_types=Currency Fragment
set item_types=DivinationCard Artifact Oil Incubator UniqueWeapon UniqueArmour UniqueAccessory UniqueFlask UniqueJewel SkillGem ClusterJewel Map BlightedMap BlightRavagedMap UniqueMap Sentinel DeliriumOrb Invitation Scarab BaseType Fossil Resonator HelmetEnchant Beast Essence Vial

echo CAPTURE_POENINJA %version% %1 %2

(for %%a in (%currency_types%) do (
	curl "https://poe.ninja/api/data/currencyoverview?league=%1&type=%%a" --output %2/%%a.json
))
(for %%a in (%item_types%) do (
	curl "https://poe.ninja/api/data/itemoverview?league=%1&type=%%a" --output %2/%%a.json
))