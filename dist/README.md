# poe-elf
<h1>Path of Exile - Economy-Linked Loot Filter</h1>

<p>
	<strong>Connor Poland</strong><br />
	github.com/connorhpoland<br />
	June 15, 2022<br />
</p>

<h2>Getting Started</h2>
<p>Path of Exile - Economy-Linked Loot Filter (Quick Start Guide)</p>

[![poe-elf-qs](https://img.youtube.com/vi/MK8llofCZBI/hqdefault.jpg)](https://youtu.be/MK8llofCZBI "Path of Exile - Economy-Linked Loot Filter (Quick Start Guide)")

<h3>Quick Start Guide</h3>
<ol>
	<li>Download Repository</li>
		<p>Using the Github (git) API, download or clone this repository onto the local filesystem.</p>
	<li>Virus Protection White-list</li>
		<p>In <strong>Windows 10</strong> it may be necissary to create a Virus and Threat Protection 'Exclusion' to allow the poe-elf.exe to run succesfully.</p>
		<ol>
			<li>Search for 'Virus and threat protection' in the Windows search bar</li>
			<li>Select 'Manage Settings'</li>
			<li>Select 'Add or remove exclusions'</li>
			<li>Select 'Add and exclusion'->'Folder'</li>
			<li>Select the dist/ directory that holds poe-elf.exe</li>
		</ol>
	<li>Configure Local dist/elf.config</li>
		<ol>
			<li>Modify 'leagueName' to desired Path of Exile League (ex. Sentinel, Sentinel HC)</li>
			<li>Modify 'filterOutputPath' to be the path to your local Path of Exile Game files (ex. C:\Users\Foo\Documents\My Games\Path of Exile\new.filter)</li>
		</ol>
	<li>Run poe-elf.exe</li>
		<p>A command prompt will open and begin running the poe-elf application. After a short time, a tone and log message will indicate a new filter is ready.
		In Path of Exile, load the generated filter file with the name configured in elf.config earlier.
		poe-elf will generate an up-to-date filter file every 15 minutes. It will be necissary to 'refresh' your loot filter in-game to utilize the latest update.</p>
</ol>

<h2>Advanced</h2>
<h3>Customizing poe.config</h3>
<p>This file contains a set on run-time configurations that will be applied to poe-elf.exe when it first starts. Besides the options described in the
<strong>Quick Start Guide</strong>, it may be unneccisary to modify any of these fields. Bellow is a detailed description of all available configuration
options. The local version of elf.config may contain any/all/none of the following options. If an option is omitted in the local elf.config it will be set to
the default value (documented bellow).</p>
<dl>
	<dt>[POE]</dt>
	<dd>Configuration options specific to Path of Exile and the local Path of Exile installation.
		<dl>
			<dt>leagueName</dt>
			<dd>Name of the Path of Exile league economy to index. This string is used to generate the HTML requests to poe.ninja.<br><em>Default: Sentinel</em></dd>
		</dl>
		<dl>
			<dt>filterOutputPath</dt>
			<dd>Path to the local Path of Exile Game files (and desired name of the filter file).<br><em>Default: ./elf.filter</em></dd>
		</dl>
	</dd>
	<dt>[LOCAL]</dt>
	<dd>Configuration options specific to the behaviour of the local Economy-Linked Loot Filter Tool.
		<dl>
			<dt>dumpDirPath</dt>
			<dd>Path to a local direcory used to hold temporary .JSON files from poe.ninja. This must be a directory that exists and can hold ~30Mbytes of data.<br><em>Default: ./tmp_poe_ninja</em></dd>
		</dl>
		<dl>
			<dt>marketIndexPath</dt>
			<dd>Path to a local file which will be created to contain a subset of data extracted from the poe.ninja .JSON data set.<br><em>Default: ./marketIndex.xml</em></dd>
		</dl>
		<dl>
			<dt>filterConfigPath</dt>
			<dd>Path to a local user configured filterConfig.xml file which contains information related to loot filter value tiers, filter display information and static filter rules. See: <strong>filterConfigs.xml.help</strong> and <strong>Customizing filterConfigs.xml</strong> bellow for further guidence on modifying this file.<br><em>Default: ./filterConfig.xml</em></dd>
		</dl>
		<dl>
			<dt>refreshInterval</dt>
			<dd>Time interval (in minutes) between the (re)generation of each dynamic Economy-Linked Loot Filter. If 0, only a single filter will be generated before the application exits - otherwise poe-elf will continue regenerate filter files until it is stopped or interrupted.<br><em>Default: 15</em></dd>
		</dl>
		<dl>
			<dt>refreshNotify</dt>
			<dd>An optional notification tone which signals that a new loot filter has been generated and is ready to be loaded (refreshed) in-game. This tone can be supressed by configuring 'no' rather than 'yes'.<br><em>Default: yes</em></dd>
		</dl>
	</dd>
	<dt>[DEBUG]</dt>
	<dd>Configuration options used for developement and troubleshooting.
		<dl>
			<dt>randomValue</dt>
			<dd>A developement utility which applies a random economic 'chaos' value to each item - this means that each in-game item will appear in a (some-what) random filter tier each time the filter is re-generated (For debug purposes only).<br><em>Default: no</em></dd>
		</dl>
		<dl>
			<dt>loggingLevel</dt>
			<dd>Describes the verbosity of the logging output (50 - CRITICAL, 40 - ERROR, 30 - WARNING, 20 - INFO, 10 - DEBUG, 0 - NOTSET). 40 (ERROR) should be sufficient to reveal most issues, however 20 (INFO) or 10 (DEBUG) will provide very detailed output for troubleshooting this and all contained modules.<br><em>Default: 40</em></dd>
		</dl>
		<dl>
			<dt>loggingLevel</dt>
			<dd>Logging output can optionally be redirected to a user configured local file rather than appearing on the poe-elf command console.<br><em>Default: NONE</em></dd>
		</dl>
	</dd>
</dl>

<h3>Customizing filterConfigs.xml</h3>
<p>This file contains blocks of filter display text (based on the Path of Exile filter API) formatted in XML sub-trees with specific XML identifiers. These XML sub-trees and identifers determine which filter display settings will be attributed to which class of item. While the display text inside the XML entries may (and should) be modified, the XML tree structure must remain as-is. Bellow is a detailed description of the configurable XML segments in filterConfigs.xml.</p>
<dl>
	<dt>&lt;configs name="Example Filter Configurations"&gt;</dt>
	<dd>
		This is the XML root, the 'name' may be modified (to decribe the contents of the configuration) but this will have no functional significance.
		<dl>
			<dt>&lt;version&gt;x.y&lt;/version&gt;</dt>
			<dd>Contains the current version of the filterConfig.xml API (for compatability reasons). Should not be modified.</dd>
		</dl>
		<dl>
			<dt>&lt;tier name="Highest Tier"&gt;</dt>
			<dd>The first (highest value) dynamic loot tier description field. XML 'tier's must be listed highest to lowest; there can be any number of 'tier' entries. The 'name' holds no functional significance besides re-inforcing the high-to-low value requirement.
				<dl>
					<dt>&lt;chaosValue&gt;x.yz&lt;/chaosValue&gt;</dt>
					<dd>The minimum value, in Chaos Orbs for an item to posses for it to appear in this dynamic loot tier. This value is a float with up-to two decimal points.</dd>
					<dt>&lt;display&gt;<dt>
					<dd>Formatted text obeying the Path of Exile filter API. This describes how an item bellonging in this tier should be displayed in-game.</dd>
				</dl>
			</dd>
		</dl>
		<dl>
			<dt>&lt;tier&gt;</dt>
			<dd>As mentioned, filterConfigs.xml can contain any number of 'tier' entries with unique 'chaosValue's and 'display' descriptions.</dd>
		</dl>
		<dl>
			<dt>&lt;tier name="Lowest Tier"&gt;</dt>
			<dd>The 'tier' entry with this name is simply reinforicng that this tier is the least valuable tier of item that will appear in-game; all items with a lower Chaos Orb value than the 'chaosValue' of this tier will be hidden.</dd>
		</dl>
		<dl>
			<dt>&lt;tier name="Hide Tier"&gt;</dt>
			<dd>The 'tier' entry with this name defines the how to display 'hidden' items using the Path of Exile filter API.</dd>
		</dl>
		<dl>
			<dt>&lt;static name="My Custom Static Entry"&gt;</dt>
			<dd>These 'static' sub-tree entries describe classes of Path of Exile items which either cannot be indexed to a specific value, are untradable or should be displayed for other in-game purposes regarless of the item's economic value. The provided filterConfigs.xml.help contains many such item classes. The User may add, remove, or modify any of these static entries for their own purposes. These static entries can have any 'name' and can describe any class of item that the Path of Exile filter API is able to describe.<br> The User should modify or remove these static entries with care as it may result in some necissary or very rare items being hidden (ex. quest items, map items, albino rhoa feathers).
				<dl>
					<dt>&lt;display&gt;</dt>
					<dd>This block of formatted text will be copied directly into the elf.filter file - this means that unlike the 'display' entry of the 'tier' tree, this 'display' item must contain a complete Path of Exile filter block (including 'Show', description of the static item class, and display information to be applied to the defined item class).</dd>
				</dl>
			</dd>
		</dl>
	</dd>
</dl>

