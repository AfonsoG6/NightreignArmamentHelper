[center][img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750104987-1353635541.png[/img][/center]

[u][b]Description[/b][/u]

[b]Nightreign Armament Helper[/b] is an Overlay mod for Elden Ring: Nightreign that is [b][color=#6aa84f]safe to use ONLINE and with EAC ENABLED[/color][/b]. It aims to help players choose the best armaments for the character they are using. It does this in a very simple manner, by displaying three separate icons directly on top of the armament's image.

[list]
[*]✔️: The weapon's stats are a [b]decent match[/b] for the character's stats.
[*]⭐: The weapon's stats are a [b]great match[/b] for the character's stats.
[*]🧤: The weapon is of the [b]type preferred[/b] by the character.
[/list]
[center][img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750103193-1130109712.png[/img]     [img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750103194-1313378343.png[/img]     [img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750103196-1270148184.png[/img][/center]

Additionally, as of version 1.1.0, the mod also provides an [b]Advanced Mode[/b] that in addition to the simple recommendation icons, also displays an armament's type and stats.

[center][img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750202311-158920342.png[/img][/center]

[i]Note:[/i] The [b]Advanced Mode[/b] being enabled does not impact performance in any way, so feel free to enable it if you prefer.

[b]Recommendations:[/b]
[list]
[*]The [b]basic mode is recommended for newer players[/b], as it is simpler and easier to understand at a glance.
[*]The [b]advanced mode is recommended for experienced players[/b] who want to see more information about the armament they are using, such as its type and stats.
[/list]

As of version 1.2.0, the mod also implements an [b]eventual responsiveness[/b] method that learns, through analysis of perfect OCR matches, a set of reference points to detect the same text in the future without having to call the OCR again. These reference points are stored in the user's %LOCALAPPDATA% folder, persisting across game sessions.

[i]Note:[/i] If the resolution of the screen is changed, the mod will have to relearn all the reference points for the new resolution.

[u][b]How to use[/b][/u]

The mod does not require any installation. Simply download the latest version of the [i]NightreignArmamentHelper.exe[/i] file from the GitHub [url=https://github.com/AfonsoG6/NightreignArmamentHelper/releases]Releases[/url] page or from [url=https://www.nexusmods.com/eldenringnightreign/mods/193?tab=files]Nexus Mods[/url] and execute it while Elden Ring: Nightreign is running.

The mod will immediately start working, attempting to detect the character being chosen and the armament being viewed.

[b]IMPORTANT[/b]: The overlay requires the game to be running in [b][color=#cc4125]BORDERLESS WINDOWED[/color][/b] mode to work correctly.

Additionally, you may verify and/or manually change the currently selected character through the very discreet dropdown menu in the top left corner of the screen.

[center][img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750103190-596967002.png[/img][/center]

Furthermore, an additional window containing a control panel for the mod will appear. This window allows you to perform the following actions:

[list]
[*]Temporarily disable/enable the mod, without closing it.
[*]Disable/enable the automatic detection of the character.
[*]Disable/enable the advanced mode, which shows additional information about the armament.
[*]Fully stop the mod.
[/list]

[center][img]https://staticdelivery.nexusmods.com/mods/7800/images/193/193-1750202318-1003327327.png[/img][/center]

[u][b]Common Questions[/b][/u]

[b]How does it work?[/b]  
The mod uses Optical Character Recognition (OCR) to detect several elements on the screen, such as the currently opened menu, the character name (only on the character selection screen), and the armament name.

It then uses this information to determine which weapon the player is currently looking at and which character they are using. Based on this information, it then displays the icons mentioned above.

It is also important to note that the mod defines the categories "great" and "decent" based on a custom mathematical algorithm, which sometimes may not match the player's expectations. If you think that a weapon should be marked as "great" or "decent" but it is not, please open an issue on GitHub.

[b]Will I get banned for using this mod?[/b]  
[color=#6aa84f][b]No[/b], you will not get banned for using this mod. The mod does not modify the game files in any way, and it does not interact with the game's memory. It simply reads the screen and displays information based on that.[/color]

[u][b]Limitations[/b][/u]

[list=1]
[*][b]Display Mode[/b]: For the overlay to be correctly shown on top of the game window, the game [color=#cc4125][b]MUST BE RUNNING IN BORDERLESS WINDOWED[/b][/color] mode.
[*][b]Ground items[/b]: Items found in the ground show their details in varying locations, making it difficult to detect them in a both efficient and accurate way. Therefore, the mod [color=#cc4125][b]DOES NOT SUPPORT THE DETECTION OF ITEMS FOUND ON THE GROUND[/b][/color]. To circumvent this, you can simply pick up the item and then open the inventory to view its details.
[*][b]Language[/b]: The mod is designed to work with the [b][color=#cc4125]ENGLISH [/color][/b]version of Elden Ring: Nightreign. It may not work correctly with other languages, as the OCR is trained on English text.
[*][b]Responsiveness[/b]: The mod is designed to be as efficient and responsive as possible, using multiple methods to avoid unnecessary OCR calls. However, it may sometimes take half a second to detect the armament and show the corresponding icons. This is due to the nature of OCR and the fact that it needs to analyze the screen in real-time.
[*][b]Accuracy[/b]: The mod uses OCR to detect text on the screen, which is not always 100% accurate. This means that it may sometimes fail to detect the armament or the character correctly. To mitigate this, we use the [i]Jaccard[/i] similarity algorithm to account for small innacuracies in the OCR results. During our testing, we found that the mod seems to always be able to detect the armament and character correctly, but there may be some edge cases where this fails.
[/list]

[u][b]Acknowledgements[/b][/u]

Thanks to [url=https://github.com/lud-berthe]lud-berthe[/url] for the original idea that inspired this mod.

Check out his mod [b]Nightreign Auto-Timer[/b] on [url=https://www.nexusmods.com/eldenringnightreign/mods/139]Nexus Mods[/url] or [url=https://github.com/lud-berthe/nightreign-auto-timer]GitHub[/url] if you haven't already.

[u][b]Source Code[/b][/u]

The source code of the project can be found on [url=https://github.com/AfonsoG6/NightreignArmamentHelper]GitHub[/url]. Feel free to contribute to the project by opening issues or pull requests.

[u][b]Support my work[/b][/u]

If you like this project and want to support its development, you can buy me a coffee through [url=https://ko-fi.com/afonsog6]Ko-fi[/url]. Thank you!

[center][url=https://ko-fi.com/afonsog6][img]https://cdn.ko-fi.com/cdn/kofi3.png[/img][/url][/center]