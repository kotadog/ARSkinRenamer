# Background
This set of files is used to maintain a mapping of Skin images in the [Atlas Reactor Fan Site Kit (FSK)](http://forums.atlasreactorgame.com/showthread.php?2209-Atlas-Reactor-Fan-Site-Kit-OFFICIAL) to the names used in the actual client. 

#Data Elements

Skin images in the FSK can be found at FSK/Skins and contain the following data elements separated by an underscore (_):

|Element|Example/Value|Description|
|-------|---------|--------|
|Style|Style|Static text that starts every skin name|
|lancer_name|Lockwood|Name of the freelancer the skin belongs to (NOTE: May not be the same as the name displayed in game)|
|skin_style_id|western|The name of the skin style.  These are specific to the FSK and not displayed in game.  This element does correllate to exactly one style of skin in game.|
|skin_id|000_001|The FSK ID of the skin variation.  Each of these correllates to exactly one skin in game.  This ID, however, is only unique within each skin_style.|

The following elements are used for the other side of mapping and can be found in the actual game client.

|Element|Example/Value|Description|
|--------|--------|--------|
|lancer_display_name|Lockwood|Name of the freelancer. (NOTE: This can be different from the name in the image file as is such in the example provided.)|
|skin_style_name|Unforgiven|Name (as displayed in game) of the matching skin style.|
|skin_name|Thunderstorm|Name (as displayed in game) of the matching skin variation.|

The data mapping includes the following elements:

![Skin Image Reference](https://github.com/kotadog/ARSkinRenamer/blob/master/images/ExampleSkinBreakdown-alternate.png)

|FSK Element|<-->|AR Client Element|
------------|----|--------------------|
|lancer_name|<-->|lancer_display_name|
|skin_style_id|<-->|skin_style_name|
|skin_id|<-->|skin_name|

These data element mappings that have already been documented in 2 filesets in this repo:
1. /csvs - easier to handle for users to be able to update information easily without having to worry about syntax
1. config.json - read by the SkinRenamer to actually rename the skins with their appropriate in-game-names.

#Script Purposes
All scripts are written using base modules using Python 2.7.13.

##SkinRenamer.py
This is the primary and original script.  Syntax and help can be found by typing SkinRenamer.py -h

Three command-line arguments are required:
|argument|description|
|---|---|
|-s|Location of skins (in FSK)|
|-l|Name of freelancer images to rename|
|-c|Location of config.json file (found in this repo)|

This script will use the config.json to rename the images and save them to a new folder (under the skins folder) called renamed using the format:
<lancer_display_name>-<skin_style_name>-<skin_name>.png - this is the convention being used by the AR wiki for file upload.

In addition, on std.out a string containing the string that should be put into the Freelancer profile on the Wiki will be displayed.  This can be copy/pasted after the images are uploaded to link the elements.

##ConfigConverter
This converts csvs to config.json or config.json to csvs.  This should be run whenenver one of the files is updated to ensure they are consistent.

Syntax:
ConfigConverter.py c2j (csv to json) - default output is to file 'config.json' in local directory.
ConfigConverter.py j2c (json to csv) - default output is to folder 'csvs' in local directory.


##
