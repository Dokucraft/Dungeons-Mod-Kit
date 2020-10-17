# Minecraft Dungeons Mod Kit

This is a set of tools to make it easier to work on mods for Minecraft Dungeons. The tools will only run on Windows.

If you are looking for tools to make resource packs for the game, check out [the `resource-packs` branch](https://github.com/Dokucraft/Dungeons-Mod-Kit/tree/resource-pack) of the mod kit.

## Prerequisites

These need to be installed in order to use the tools:

- [Python 3.8+](https://www.microsoft.com/en-us/p/python-38/9mssztt1n39l)
- Unreal Engine 4.22

You can download Unreal Engine for free through the Epic Games Store app, just **make sure to select version 4.22.x**. Using a different version of UE4 will cause all sorts of strange issues.

## Example Files

There are a few example files included with these tools that you may want to remove if you're making your own mod:

- Dungeons/Content/data/resourcepacks/squidcoast/blocks.json
- UE4Project/Content/Decor/Prefabs/Lever/T_Lever.png
- UE4Project/Content/Decor/Prefabs/Lever/T_Lever.uasset

You can automatically remove these using the `Tools/clean_up_mod_kit.bat` tool.

## Setup

Edit the text files in the `Tools/user_settings` folder to configure the tools:

| File                    | Description   |
| ----------------------- | ------------- |
| editor_directory.txt    | This contains the path to the folder where the Unreal Editor executables are. |
| package_output.txt      | This contains the path to the .pak file that the package.bat tool creates. |

Setting the package_output path to a file in your `~mods` folder is recommended to make testing the mod easy.

By default, materials are configured to not be packaged. If you want to change that, or if you want to exclude other Unreal assets from being packaged, you can edit `Tools/configs/copy_cooked_assets.rcj`. To include materials, just remove `M_*.u*` and `MI_*.u*`. To exclude certain files, just add the file names at the bottom, each on their own line. If you remove all of the filters, you need to remove `/XF` as well.

## How to use the tools

This guide assumes you're already familiar with the game files and how to [extract them.](https://docs.dungeonsworkshop.net/creatingmods/#extracting-game-files)

### Unreal Assets

Any 3D model, sound file, texture that isn't a block texture, and a bunch of other things are *Unreal assets*. These files should be managed using the Unreal editor. You can open the project by opening the `Dungeons.uproject` file in the `UE4Project` folder using the editor.

Unreal assets need to be *cooked* before being packaged.

#### Cooking

Run the `cook_assets.bat` tool to cook the assets and automatically copy them to the `Dungeons` folder, ready to be packaged.

You can exclude certain files by editing `Tools/configs/copy_cooked_assets.rcj`, like mentioned in the **Setup** section above. By default, material files are excluded.

#### Precooked Files

For Unreal assets that are already cooked, for example modified blueprint .uasset files, you can put them in the `Precooked` folder and they will automatically be added when running the `cook_assets.bat` tool. If you don't have a `Precooked` folder, simply make one in the root folder of the mod kit, next to `Dungeons`, `UE4Project`, `package.bat`, etc.

Note that any cooked assets you put directly in the `Dungeons` folder will be deleted when running the `cook_assets.bat` tool because it needs to clean up the old assets before copying the new ones into the folder.

### Other Files

Anything that isn't an Unreal asset, like level .json files, should be added to the `Dungeons` folder. This folder is what will be turned into a .pak file.

### Packaging

To test your mod, you can run the `package.bat` tool to create a .pak file. If the tool is configured to place the .pak file in your `~mods` folder, you can start the game as soon as it finishes.

To package your mod for release, use the `Tools/pack_compressed.bat` tool instead. This tool will create a `compressed_pack.pak` file in your `Tools` folder. This .pak file usually takes slightly longer to create, but the file size should be much smaller. You can rename the .pak file to whatever you want.