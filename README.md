# Minecraft Dungeons Mod Kit

This is a set of tools to make it easier to work on mods for Minecraft Dungeons. The tools will only run on Windows.

## Prerequisites

These need to be installed in order to use the tools:

- [Python 3.8+](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l)
- Unreal Engine 4.22

You can download Unreal Engine for free through the Epic Games Store app, just make sure to select version 4.22.x. Using a different version of UE4 will cause all sorts of strange issues.

## Setup

Edit the text files in the `Tools/user_settings` folder to configure the tools:

| File                    | Description   |
| ----------------------- | ------------- |
| editor_directory.txt    | This contains the path to the folder where the Unreal Editor executables are. |
| package_output.txt      | This contains the path to the .pak file that the package.bat tool creates. |
| quickbms_export_dir.txt | This contains the path to the folder where you have exported the game files using QuickBMS. This is only needed for the `Tools/copy_missing_blocks.bat` and `Tools/update_block_textures_config.bat` tools. |

Setting the package_output path to a file in your `~mods` folder is recommended to make testing the mod easy.

By default, materials are configured to not be packaged. If you want to change that, or if you want to exclude other Unreal assets from being packaged, you can edit `Tools/configs/copy_cooked_assets.rcj`. To include materials, just remove `M_*.u*` and `MI_*.u*`. To exclude certain files, just add the file names at the bottom, each on their own line. If you remove all of the filters, you probably need to remove `/XF` as well.

## Example Files

There are a few example files included with these tools that you may want to remove if you're making your own mod:

- Block Textures/grass_side.png
- Dungeons/Content/data/resourcepacks/squidcoast/blocks.json
- UE4Project/Content/Decor/Prefabs/Lever/T_Lever.png
- UE4Project/Content/Decor/Prefabs/Lever/T_Lever.uasset

You can automatically remove these using the `Tools/clean_up_mod_kit.bat` tool.

## How to use the tools

This guide assumes you're already familiar with the game files and how to [extract them.](https://docs.dungeonsworkshop.net/creatingmods/#extracting-game-files)

### Block Textures

The game uses different resource packs depending on the level you're playing. For example, the tutorial mission and the camp uses a pack called `squidcoast`, while the Redstone Mines level uses the `mooncorecaverns` pack. Since the game's resource packs share a lot of textures, you would normally have to copy a few hundred textures and paste them into each pack folder, but this is something these tools tries to fix.

To make it easier to manage, these tools use just a single folder for all block textures in all of the packs, called `Block Textures`. The textures will be automatically copied to the right place(s) when you run the `build_resource_packs.bat` tool. The file names in the `Block Textures` folder are slightly different because the game might use 3 or 4 different textures for the same block in different packs. You can find all of the files names in `Tools/configs/block_textures.json` and what files in the resource packs they represent. You can also edit this file to change the file names, or to add more textures. Running the `Tools/print_missing_blocks.bat` tool will show you a list of block textures that *aren't* in the `Block Textures` folder, as well as the number of missing files. If you want to see all of the block textures that you are missing in a folder instead, use `Tools/copy_missing_blocks.bat`, which will create a `Missing Textures` folder in the root folder of the mod kit with all of the vanilla block textures that aren't replaced by your textures in `Block Textures` yet.

The default `Tools/config/block_textures.json` file uses one texture for textures that are very similar. For example, the game uses the same texture for dirt in several of the packs, but it's very slightly changed to be a different hue or brightness. If the textures are similar enough, the default configuration will use one texture for all of them. If you want to use different textures for each, you'll have to edit the `Tools/configs/block_textures.json` file.

If an update for the game comes out and you don't want to wait for the mod kit to update, you can use the `Tools/update_block_textures_config.bat` tool to update it yourself. It requires the QuickBMS exported files of the game, and [Pillow](https://pypi.org/project/Pillow/), so make sure that is installed before you run it. After it's done, the block textures config should be updated.

### Unreal Assets

Any 3D model, sound file, texture that isn't a block texture, and a bunch of other things are *Unreal assets*.

Unreal assets needs to be *imported* and *cooked* by the Unreal editor before being packaged. To do this, they need to be put in the `UE4Project/Content` folder. The folder structure here should be the same as the Content folder from the extracted game files.

Like the block textures, there is a tool for showing a list of missing Unreal textures: `Tools/print_missing_actors_prefabs.bat` However, like the name suggests, it only prints the missing textures in the `Actors` and `Decor/Prefabs` folders instead of all Unreal textures.

#### Importing

Once the files are in the right place, you need to import them. For textures and static models, this can be done by simply double clicking the `import_assets.bat` tool. If you edit the texture/model after importing, you have to reimport it, which can be done by deleting the .uasset file with the same name and then running the import tool again.

For things that *aren't* textures or static models, you have to import them using the Unreal Editor. You can open the project in the editor by double clicking the `Dungeons.uproject` file in the `UE4Project` folder. If you're not familiar with the editor, don't worry, most of the time the editor will automatically notice the files you add to the folder and ask if you want to import them.

If you import textures using the editor instead of the `import_assets.bat` tool, you'll also have to double click the texture in the file brower in the editor and then change the compression setting to BC7 and the texture group to `2D Pixels (Unfiltered)`. Not doing this will make pixel art textures look blurry in-game.

#### Cooking

Once the assets have been imported, it's time to "cook" them. This is done by simply double clicking the `cook_assets.bat` tool. The tool will cook the assets and copy them to the `Dungeons` folder, ready to be packaged.

You can exclude certain files by editing `Tools/configs/copy_cooked_assets.rcj`, like mentioned in the **Setup** section above. By default, material files are excluded.

#### Precooked Files

For Unreal assets that are already cooked, for example modified blueprint .uasset files, you can put them in the `Precooked` folder and they will automatically be added when running the `cook_assets.bat` tool.

Note that any cooked assets you put directly in the `Dungeons` folder will be deleted when running the `cook_assets.bat` tool because it needs to clean up the old assets before copying the new ones into the folder.

### Other Files

Anything that isn't a block texture or Unreal asset, like level .json files, should be added to the `Dungeons` folder. This folder is what will be turned into a .pak file.

### Packaging

To test your mod, you can run the `package.bat` tool to create a .pak file. If the tool is configured to place the .pak file in your `~mods` folder, you can start the game as soon as it finishes.

To package your mod for release, use the `Tools/pack_compressed.bat` tool instead. This tool will create a `compressed_pack.pak` file in your `Tools` folder. This .pak file usually takes slightly longer to create, but the file size should be much smaller. You can rename the .pak file to whatever you want.

### TL;DR

- Run the `build_resource_packs.bat` tool after editing anything in `Block Textures`.
- Put source files for Unreal assets in `UE4Project/Content`, then import them using the `import_assets.bat` tool or the Unreal Editor.
- Use the `cook_assets.bat` tool after importing new Unreal assets.
- For testing, use `package.bat`. Use `Tools/pack_compressed.bat` instead when you want to package the mod for release.

### Other Useful Tools

- The `Tools/completion_stats.bat` tool will show the statistics that the `print_missing_*` tools do, but will also show combined stats.
- The `Tools/clean_up_mod_kit.bat` tool will delete all mod files from the mod kit folder. This can useful if you are making a lot of smaller mods. Be careful with it, though. It does ask you to confirm before it starts deleting things, but it doesn't make any backups once it starts deleting.
- The `Tools/delete_redundant_block_textures.bat` tool will delete all redundant textures in the `Block Textures` folder. Redundant textures are files that are not in the `Tools/configs/block_textures.json` config, meaning they are not actually being used at all.