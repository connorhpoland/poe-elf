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

<ol>
	<li>Download Repository</li>
	<li>Whitelist dist Directory</li>
		<p>In <strong>Windows 10</strong> it may be necissary to create a Virus and Threat Protection 'Exclusion' to allow the poe-elf.exe to run succesfully.</p>
		<ol>
			<li>Search for 'Virus and threat protection' in the Windows search bar</li>
			<li>Select 'Manage Settings'</li>
			<li>Select 'Add or remove exclusions'</li>
			<li>Select 'Add and exclusion'->'Folder'</li>
			<li>Select the dist/ directory that holds poe-elf.exe</li>
		</ol>
	<li>Configure Local dist/elf.config</li>
		<ol>Modify 'leagueName' to desired Path of Exile League (ex. Sentinel, Sentinel HC)</ol>
		<ol>Modify 'filterOutputPath' to be the path to your local Path of Exile Game files (ex. C:\Users\Foo\Documents\My Games\Path of Exile\new.filter) </ol>
	<li>Run poe-elf.exe</li>
		<p>A command prompt will open and begin running the poe-elf application. After a short time, a tone and log message will indicate a new filter is ready.</p>
		<p>In Path of Exile, load the generated filter file with the name configured in elf.config earlier.</p>
		<p>poe-elf will generate an up-to-date filter file every 15 minutes. It will be necissary to 'refresh' your loot filter in-game to utilize the latest update.</p>
</ol>

<h2>Advanced</h2>
<h3>poe.config</h3>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This file contains a set on run-time configurations that will be applied to poe-elf.exe when it first starts.</p>

