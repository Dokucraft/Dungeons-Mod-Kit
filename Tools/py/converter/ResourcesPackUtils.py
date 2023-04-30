import tempfile
from shutil import copy2, make_archive
from pathlib import Path
import BlockMap as BlockMap
from os import makedirs, path

"""
MCD = MineCraft Dungeon
MCJ = MineCraft Java
"""

MCD_PACK_ICON = "pack_icon.png"
MCJ_PACK_ICON = "pack.png"
MCJ_PACK_META = "pack.mcmeta"

MCD_BLOCK_FOLDER = path.join("images", "blocks")
MCJ_BLOCK_FOLDER = path.join("assets", "minecraft", "textures", "block")

additional_dict = {
    'stonebrick': 'stone_bricks',
    'stonebrick_mossy': 'mossy_stone_bricks',
    'stonebrick_cracked': 'cracked_stone_bricks',
    'stonebrick_carved': 'chiseled_stone_bricks',
    'stonefloor1': 'blackstone',
    'stonefloor2': 'chiseled_polished_blackstone',
    'stonefloor3': 'polished_blackstone',
    'stonefloor4': 'polished_blackstone_bricks',
    'stonefloor5': 'gilded_blackstone',
    'stonefloor6': 'cracked_polished_blackstone_bricks',
    'stonefloor7': 'lodestone',
    'stonefloor8': 'ancient_debris',
    'stonefloor9': 'infested_chiseled_stone_bricks',
    'stone_andesite': 'andesite',
    'stone_andesite_smooth': 'polished_andesite',
    'stone_diorite': 'diorite',
    'stone_diorite_smooth': 'polished_diorite',
    'stone_slab_side': 'smooth_stone_slab_side',  # Not sure
    'tallgrass': 'grass',
    'tnt_bottom': 'tnt_bottom',
    'tnt_top': 'tnt_top',
    'tnt_side': 'tnt_side',
    'torch_on': 'torch',
    'redstone_torch_on': 'redstone_torch',
    'trapdoor': 'oak_trapdoor',
    'waterlily': 'lily_pad',
    'wheat_stage_0': 'wheat_stage0',
    'wheat_stage_1': 'wheat_stage1',
    'wheat_stage_2': 'wheat_stage2',
    'wheat_stage_3': 'wheat_stage3',
    'wheat_stage_4': 'wheat_stage4',
    'wheat_stage_5': 'wheat_stage5',
    'wheat_stage_6': 'wheat_stage6',
    'wheat_stage_7': 'wheat_stage7',
    'wool_colored_white': 'white_wool',
    'wool_colored_yellow': 'yellow_wool',
    'wool_colored_red': 'red_wool',
    'wool_colored_purple': 'purple_wool',
    'wool_colored_pink': 'pink_wool',
    'wool_colored_orange': 'orange_wool',
    'wool_colored_magenta': 'magenta_wool',
    'wool_colored_lime': 'lime_wool',
    'wool_colored_green': 'green_wool',
    'wool_colored_light_blue': 'light_blue_wool',
    'wool_colored_gray': 'gray_wool',
    'wool_colored_cyan': 'cyan_wool',
    'wool_colored_brown': 'brown_wool',
    'wool_colored_blue': 'blue_wool',
    'wool_colored_black': 'black_wool',
    'anvil_base': 'anvil',
    'anvil_top_damaged_0': 'anvil_top',
    'anvil_top_damaged_1': 'chipped_anvil_top',
    'anvil_top_damaged_2': 'damaged_anvil_top',
    'beacon': 'beacon',
    'beetroot_stage_0': 'beetroot_stage_0',
    'beetroot_stage_1': 'beetroot_stage_1',
    'beetroot_stage_2': 'beetroot_stage_2',
    'beetroot_stage_3': 'beetroot_stage_3',
    'brewing_stand_base': 'brewing_stand_base',
    'brick': 'bricks',
    'cactus_bottom': 'cactus_bottom',
    'cactus_top': 'cactus_top',
    'cactus_side': 'cactus_side',
    'cake_bottom': 'cake_bottom',
    'cake_inner': 'cake_inner',
    'cake_side': 'cake_side',
    'cake_top': 'cake_top',
    'carrots_stage_0': 'carrots_stage0',
    'carrots_stage_1': 'carrots_stage1',
    'carrots_stage_2': 'carrots_stage2',
    'carrots_stage_3': 'carrots_stage3',
    'cauldron_bottom': 'cauldron_bottom',
    'cauldron_inner': 'cauldron_inner',
    'cauldron_side': 'cauldron_side',
    'cauldron_top': 'cauldron_top',
    'cobblestone_mossy': 'mossy_cobblestone',
    'cocoa_stage_0': 'cocoa_stage0',
    'cocoa_stage_1': 'cocoa_stage1',
    'cocoa_stage_2': 'cocoa_stage2',
    'comparator_on': 'comparator_on',
    'comparator_off': 'comparator',
    'crafting_table_front': 'crafting_table_front',
    'crafting_table_side': 'crafting_table_side',
    'crafting_table_top': 'crafting_table_top',
    'custom_0': 'white_concrete',
    'custom_1': 'orange_concrete',
    'custom_2': 'magenta_concrete',
    'custom_3': 'light_blue_concrete',
    'custom_4': 'yellow_concrete',
    'custom_5': 'lime_concrete',
    'custom_6': 'pink_concrete',
    'custom_7': 'gray_concrete',
    'custom_8': 'light_gray_concrete',
    'custom_9': 'cyan_concrete',
    'custom_10': 'blue_concrete',
    'custom_11': 'purple_concrete',
    'custom_12': 'brown_concrete',
    'custom_13': 'green_concrete',
    'custom_14': 'red_concrete',
    'custom_15': 'black_concrete',
    'daylight_detector_inverted_top': 'daylight_detector_inverted_top',
    'daylight_detector_side': 'daylight_detector_side',
    'daylight_detector_top': 'daylight_detector_top',
    'deadbush': 'dead_bush',
    'destroy_stage_0': 'destroy_stage_0',
    'destroy_stage_1': 'destroy_stage_1',
    'destroy_stage_2': 'destroy_stage_2',
    'destroy_stage_3': 'destroy_stage_3',
    'destroy_stage_4': 'destroy_stage_4',
    'destroy_stage_5': 'destroy_stage_5',
    'destroy_stage_6': 'destroy_stage_6',
    'destroy_stage_7': 'destroy_stage_7',
    'destroy_stage_8': 'destroy_stage_8',
    'destroy_stage_9': 'destroy_stage_9',
    'dirt_path_side': 'grass_path_side',
    'dirt_path_top': 'grass_path_top',
    'dispenser_front_horizontal': 'dispenser_front',
    'dispenser_front_vertical': 'dispenser_front_vertical',
    'door_acacia_lower': 'acacia_door_bottom',
    'door_acacia_upper': 'acacia_door_top',
    'door_birch_lower': 'birch_door_bottom',
    'door_birch_upper': 'birch_door_top',
    'door_dark_oak_lower': 'dark_oak_door_bottom',
    'door_dark_oak_upper': 'dark_oak_door_top',
    'door_iron_lower': 'iron_door_bottom',
    'door_iron_upper': 'iron_door_top',
    'door_jungle_lower': 'jungle_door_bottom',
    'door_jungle_upper': 'jungle_door_top',
    'door_spruce_lower': 'spruce_door_bottom',
    'door_spruce_upper': 'spruce_door_top',
    'door_wood_lower': 'oak_door_bottom',
    'door_wood_upper': 'oak_door_top',
    'grass_top': 'grass_block_top',
    'grass_side': 'grass_block_side',
    'grass_path_top': 'grass_path_top',
    'grass_path_side': 'grass_path_side',
    'dirt_podzol_top': 'podzol_top',
    'dirt_podzol_side': 'podzol_side',
    'mycelium_side': 'mycelium_side',
    'mycelium_top': 'mycelium_top',
    'log_big_oak': 'oak_log',
    'log_big_oak_top': 'oak_log_top',
    'leaves_oak': 'oak_leaves',
    # TODO: finish the list (A lot more to do)
}

"""
Ignored:
    stonecutter_top (size not matching)
    stonecutter_side (size not matching)
    stonecutter_other_side (size not matching)
    stonecutter_bottom (size not matching)
    stone_gradient_{0..15}
    stone_path_side
    stone_path_top
    stone_slab_top
    tallgrass
    torch_on_emissive
    transparent
    trip_wire
    trip_wire_source
    wool_colored_silver
    _end_stone
    bed_feet_end
    bed_feet_side
    bed_feet_top
    bed_head_end
    bed_head_side
    bed_head_top
    build_allow
    build_deny
    camera_back
    camera_front
    camera_side
    camera_top
    carried_waterlily
    cauldron_water
    chest_front
    chest_side
    chest_top
    command_block
    diamond_ore_emissive
    dirt_podzol_side
    dirt_podzol_top
    grass_and_leaves_27
    _grass_side
"""


class DungeonToJavaResourcesPack:

    def __init__(self, resource_pack_path, dest_path, verbose=False):
        self.dest_path = dest_path
        self.verbose = verbose
        self.path = resource_pack_path
        if verbose:
            print("from ", self.path, " to ", self.dest_path)

    def convert(self):
        # Creating temp folder to store the resources
        f = tempfile.TemporaryDirectory()

        if self.verbose:
            print("Temp directory created ", f.name)

        # Creating directory to store blocks textures
        makedirs(path.join(f.name, MCJ_BLOCK_FOLDER))

        # Copying icon pack
        copy2(path.join(self.path, MCD_PACK_ICON), path.join(f.name, MCJ_PACK_ICON))

        # Creating meta description file
        meta = open(path.join(f.name, MCJ_PACK_META), "w")
        meta.write('{ "pack": { "pack_format": 5, "description": "auto generated resources pack" } }')
        meta.close()

        # Take all textures (.png) from the directory give. TODO: convert TGA
        blocks_path = Path(path.join(self.path, MCD_BLOCK_FOLDER)).glob('*.png')

        # Iterate though all blocs
        for block in blocks_path:
            # Try to found the id
            java_block = BlockMap.blocks_by_java_id.get("minecraft:" + block.stem)
            if java_block is not None:
                block_name = java_block[0]['java'][0]
                # Cpy in the directory
                copy2(block.absolute(), path.join(f.name, MCJ_BLOCK_FOLDER, block_name[10:len(block_name)] + ".png"))
            else:
                # Check the additional dict
                java_block = additional_dict.get(block.stem)

                if java_block is not None:
                    # Cpy in the directory
                    copy2(block.absolute(), path.join(f.name, MCJ_BLOCK_FOLDER, java_block + ".png"))
                elif self.verbose is True:
                    print(block.stem, " not recognized")
        # Create the archive
        make_archive(self.dest_path, 'zip', f.name)

        # delete the temp directory
        f.cleanup()

