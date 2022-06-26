# poe-elf
<h1>Path of Exile - Economy-Linked Loot Filter</h1>

<p>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>Connor Poland</strong><br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;github.com/connorhpoland<br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;June 15, 2022<br />
</p>

<h2>Environment</h2>
	<p>Windows 10 Home 21H1 19043.1706<br />
	Python 3.9.7<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This tool utilizes pyinstaller to hopefully package all dependancies in our .exe<br />

<h2>Summary</h2>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This project serves as a proof-of-concept/prototype for a compainon tool to the game Path of Exile. Fundamentilly, this project is a composite of two standalone tools:<br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1) Index Generator: A program that is able to aggregate and parse data associated with the current state of the real-time in-game economy and then output that data into a formatted file.<br />
		&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;and<br />
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2) Dynamic Filter Generator: An (ideally) light-weight tool that parses the output of 1) and generates a 'Loot Filter' based on user defined value requirements. https://www.pathofexile.com/developer/docs/reference#itemfilters</p>
		
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path of Exile provides the ability for players to place items in 'Public Stashes' with a 'Trade' price. All items in all player configured 'Public Stashes' are added to a global database which other player can query for the purpose of aquiring desirable in-game items. https://www.pathofexile.com/developer/docs/reference#publicstashes<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This means that it is possible to issue a set of queries to the public database to determine the expected/average 'Trade' value of a specific item, or class of item. With a large enough set of queries, a 'Snapshot' or index can be generated which will reflect the current value of all in-game items.
Fortunatly, https://poe.ninja/ already offers a rather complete and accurate real-time market index we can use for this purpose.</p>

<h2>Demo</h2>
<p>Path of Exile - Economy-Linked Loot Filter (First Demo)</p>

[![poe-elf-demo](https://img.youtube.com/vi/x8C3kRLIXEw/hqdefault.jpg)](https://youtu.be/x8C3kRLIXEw "Path of Exile - Economy-Linked Loot Filter (First Demo)")

<h2>Description</h2>
<h3>poe-elf.py</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The entry point for this tool. TODO - command line opts</p>
<h3>elf.config</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;User modifiable config file that defines the behaviour of <strong>poe-elf.py</strong></p>
<h3>capture_poeninja.py</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python program utilizing CURL-like HTTP requests to download poe.ninja market data. This script takes two arguments, league name (ie. Sentinel) and output directory to be populated with .JSON files</p>
<h3>filterConfigs.xml.help</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A barebones example filterConfigs.xml. This file contains configurable information related to the the generation of the loot filter including - Number of loot tiers, value associated with each loot tier, and display information for both dynamic and static filter rules</p>
<h3>filterGen.py</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python program which generates a new Path of Exile filter file based on a market snapshot file of form <strong>marketIndex.xml.help</strong>, and filter configuration file of form <strong>filterConfigs.xml.help</strong>. The resulting economy-linked loot filter file can be loaded into Path of Exile through the in-game settings</p>
<h3>marketIndex.xml.help</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A more readable example marketIndex.xml file with in-line comments to describe format requirements. This is not a complete index file.</p>
<h3>ninja_indexGen.py</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python program which takes a set of .JSON files generated by <strong>capture_poeninja.bat</strong> that represent a snapshot of the Path of Exile economy and produces a reduced .xml version of that data set in the form of <strong>marketIndex.xml.help</strong></p>
<h3>rand_indexGen.py</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python program very similar to <strong>ninja_indexGen.py</strong>. Instead of deriving item value from poe.ninja, this program randomly generates the value of each item - this can be used to debug/demo the dynamic nature of this tool</p>

<h2>Limitations</h2>
<h3>Index Generator</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Just as in a traditional economy, players with sufficient resources and knowledge of the trade API are able to distort or influence the in-game economy to make very valuable items appear less valuable or vice-versa. This means that our market index will have limited accuracy - ultimately causing situations where other-wise valuable in-game items may be hidden from user of this tool.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The prototype of this tool is heavily utilizing the existing https://poe.ninja tool to aggregate item values which means the stability of this tool will be dependant on the specific API of this websites (poe.ninja API documentation https://github.com/5k-mirrors/misc-poe-tools/blob/master/doc/poe-ninja-api.md). We will utilize CURL-style HTTP requests (from the request python module) to requests to GET a set of JSON files from poe.ninja as the starting point for our index.</p>
<h3>Dynamic Filter Generator</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The primary limitation of this tool (and every 'dynamic' loot filter tool) is that Path of Exile loot filters at stored as a file which is statically loaded and applied to your character when you log-in and it is not updated until the character logs in again or the filter is manually refreshed from the in-game menu. The Path of Exile economy can fluctuate drastically within minutes-to-hours and the fast-pased nature of the game makes it unlikely that a player will be regularly willing to 're-log' or paw through nested setting menues every few minutes. While it is outside the scope of the prototype it may be possible to create a periodic/schedulable macro that can instantly access the in-game menu and refresh the loot filter without disrupting gameplay.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Path of Exile is updated with a major patch quarterly and it is possible (very likely) that these patches will add or modify in-game items or item properties. This means that the Dynamic Filter Generator tool will require quarterly updates to stay usable. The prototype will reflect the in-game filter format imposed by Path of Exile 3.18.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Besides in-games items which can be linked to an external market value, there are a number of in-game items which hold limited to no 'Trade' value but must not be hidden in a players loot filter for certain aspects of the game to function - these items must be statically filtered or filtered by some user-preference rather than market value.<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This tool prototype will also not officially support Standard leagues due to increased complexity of legacy items.</p>

<h2>Future Features</h2>
<h3>Linux Support</h3>
		<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This tool has evolved to utilize stictly Python due to it's nearly trivial portability to Linux. Maintaining Windows and Linux support is intuative as Path of Exile itself if played on both platforms.</p>
<h3>User Experience</h3>
		<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;filterConfigs.xml requires a high level of user knowledge and is not as intuative to modify as other static filter tools Path of Exile players are firmilair with. A UI or additional abstraction layer on this API would be valuable to make this tool more usable/customizable - especially as Path of Exile grows in complexity and the number of 'special' cases explodes.</p>
<h3>Stackable Currency</h3>
		<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Currently, we evaluate loot drops as single items however like-currencies are able to drop in stacks. This means you can loot several stacked items in a single click. It goes without saying that the value of a stack of currency is the value of the item times the stack size. In this way we may need to re-tier an item stack if the whole stack falls into a different catagory. Ex. 1 Chaos orb may appear in the lowest filter tier however a stack of 10 Chaos Orbs should be displayed in a higher tier with other items valued ~10 Chaos.</p>
<h3>Basic Recipes</h3>
		<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Path of Exile, some items with specific properties can be trivially exchanged in-game for other valuable items (ex. Any 6-Linked item can be sold to any in-game vendor for 1 Divine Orb). This means that there are items that are currently staticly filtered which could instead be mapped to another dynamically indexed item.</p>
