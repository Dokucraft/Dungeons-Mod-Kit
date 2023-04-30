"""A collection of tools that convert Dungeons tiles to other formats and vice versa."""

import os
import time
import json
import re

import anvil
from nbt.nbt import *
from PIL import Image

from pretty_compact_json import stringify
from JavaWorldReader import JavaWorldReader
from Tile import Tile, Boundary, Door, Region
from BlockMap import find_java_block, find_dungeons_block
from ResourcesPackUtils import DungeonToJavaResourcesPack
def find_tile_entity(chunk, x, y, z):
  for te in chunk.tile_entities:
    if te['x'].value == x and te['y'].value == y and te['z'].value == z:
      return te
  return None

def structure_block_entity(x, y, z, mode='DATA', name='', metadata='', px=0, py=0, pz=0, sx=0, sy=0, sz=0):
  tile_entity = TAG_Compound()
  tile_entity.tags.extend([
    TAG_String(name='author', value='?'),
    TAG_String(name='id', value='minecraft:structure_block'),
    TAG_Byte(name='ignoreEntities', value=1),
    TAG_Float(name='integrity', value=1),
    TAG_Byte(name='keepPacked', value=0),
    TAG_String(name='metadata', value=metadata),
    TAG_String(name='mirror', value='NONE'),
    TAG_String(name='mode', value=mode),
    TAG_String(name='name', value=name),
    TAG_Int(name='posX', value=px),
    TAG_Int(name='posY', value=py),
    TAG_Int(name='posZ', value=pz),
    TAG_Byte(name='powered', value=0),
    TAG_String(name='rotation', value='NONE'),
    TAG_Long(name='seed', value=0),
    TAG_Byte(name='showair', value=0),
    TAG_Byte(name='showboundingbox', value=0),
    TAG_Int(name='sizeX', value=sx),
    TAG_Int(name='sizeY', value=sy),
    TAG_Int(name='sizeZ', value=sz),
    TAG_Int(name='x', value=x),
    TAG_Int(name='y', value=y),
    TAG_Int(name='z', value=z)
  ])
  return tile_entity

# Colors for the plane images
region_plane_colors = [
  ( 98, 188,  50), # Walkable, minimap
  (237, 214,  59), # Walkable, no minimap
  (  0,   0,   0), # Unwalkable, no minimap, used for big falls
  ( 25, 155, 216), # Walkable, minimap, used for overhangs/tunnels
  (244,  38,  16), # Unwalkable, no minimap, used for walls
]
region_plane_color_names = [
 'Walkable, minimap, used for most playable areas',
 'Walkable, no minimap, used for playable areas that are not on the minimap',
 'Unwalkable, no minimap, used for big falls',
 'Walkable, minimap, used for overhangs/tunnels',
 'Unwalkable, no minimap, used for walls',
]

def closest_color(rgb, palette):
  r, g, b = rgb
  color_diffs = []
  for color in palette:
    cr, cg, cb = color
    color_diff = sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
    color_diffs.append((color_diff, color))
  return min(color_diffs)[1]

class JavaWorldToObjectGroup:
  """Converter that takes a Java Edition world and creates a Dungeons object group."""
  def __init__(self, world_dir):
    self.world_dir = world_dir
    self.boundary_block = 'minecraft:barrier'

  def convert(self, dict_format=True):
    """Returns a Dungeons object group, or a list of tiles, based on the Java Edition world."""
    with open(self.world_dir + '/objectgroup.json') as json_file:
      tiles = [Tile.from_dict(t) for t in json.load(json_file)['objects']]

    world = JavaWorldReader(self.world_dir)

    air_blocks = [
      'minecraft:air',
      'minecraft:cave_air'
    ]

    player_heads = [
      'minecraft:player_head',
      'minecraft:player_wall_head'
    ]

    # Apologies for the confusing variable names below. Let me explain what they mean:
    #   ax, ay, az are absolute coordinates. These are the world coordinates of the block in Java edition.
    #   tx, ty, tz are block coordinates relative to the tile's position.
    #   cx and cz are chunk coordinates. Chunks hold 16x256x16 blocks.
    #   yi and zi are iterable ranges for the Y and Z axes.

    for tile in tiles:
      # Creating these ranges here is faster than doing it for each slice/column of the tile
      zi = range(tile.size[2])
      yi = range(min(256, tile.size[1]))

      doors = []

      # For each slice of the tile along the X axis...
      for tx in range(tile.size[0]):
        ax = tx + tile.pos[0]
        cx = ax // 16

        # For each column of the slice along the Z axis...
        for tz in zi:
          az = tz + tile.pos[2]
          cz = az // 16
          chunk = world.chunk(cx, cz)
          if chunk is None:
            print(f'Warning: Missing chunk at {cx},{cz}. Blocks in this chunk will be ignored.')
            continue

          # TODO: Handle boundaries differently. With the current implemenation,
          # boundaries that go outside of the tile (most of the vanilla ones do...)
          # will lose the parts that are outside of the tile.
          current_boundary = None

          # For each block in the column along the Y axis...
          for ty in yi:
            ay = ty + tile.pos[1]

            # Get the block from the Java world chunk
            java_block = chunk.get_block(ax % 16, ay, az % 16)
            namespaced_id = java_block.namespace + ':' + java_block.id

            # There's no reason to keep going if the block is just air
            if namespaced_id in air_blocks:
              continue

            # Handle blocks that are used for special things in this converter, like tile doors and boundaries
            if namespaced_id == 'minecraft:structure_block':
              entity = find_tile_entity(chunk, ax, ay, az)
              if entity is None:
                continue

              if entity['name'].value.startswith('door:'):
                door = Door(
                  pos = [tx + entity['posX'].value, ty + entity['posY'].value, tz + entity['posZ'].value],
                  size = [entity['sizeX'].value, entity['sizeY'].value, entity['sizeZ'].value])
                if len(entity['name'].value) > 5:
                  door.name = entity['name'].value[5:]
                if len(entity['metadata'].value) > 2:
                  try:
                    door_info = json.loads(entity['metadata'].value)
                    if 'tags' in door_info:
                      door.tags = door_info['tags']
                  except:
                    print(f'Warning: Invalid JSON in structure block metadata at {ax},{ay},{az}')
                tile.doors.append(door)

              elif entity['name'].value.startswith('region:'):
                tile_region = Region( # Note: This is a Tile.Region, not an anvil.Region
                  pos = [tx + entity['posX'].value, ty + entity['posY'].value, tz + entity['posZ'].value],
                  size = [entity['sizeX'].value, entity['sizeY'].value, entity['sizeZ'].value])
                if len(entity['name'].value) > 7:
                  tile_region.name = entity['name'].value[7:]
                if len(entity['metadata'].value) > 2:
                  try:
                    region_info = json.loads(entity['metadata'].value)
                    if 'tags' in region_info:
                      tile_region.tags = region_info['tags']
                    if 'type' in region_info:
                      tile_region.type = region_info['type']
                  except:
                    print(f'Warning: Invalid JSON in structure block metadata at {ax},{ay},{az}')
                tile.regions.append(tile_region)
              continue

            if namespaced_id in player_heads:
              tile_region = Region([tx, ty, tz]) # Note: This is a Tile.Region, not an anvil.Region
              tile_region.name = 'playerstart'
              tile_region.tags = 'playerstart'
              tile_region.type = 'trigger'
              tile.regions.append(tile_region)
              continue

            if namespaced_id == self.boundary_block:
              # Check if this block is connected to the last boundary found in this column
              if current_boundary is None or current_boundary.y + current_boundary.h != ty:
                current_boundary = Boundary(tx, ty, tz, 1)
                tile.boundaries.append(current_boundary)
              else:
                current_boundary.h += 1
              continue

            # Mapped blocks have both a Java namespaced ID + state and a Dungeons ID + data value
            mapped_block = find_java_block(java_block)

            if mapped_block is None:
              props = {}
              for prop in java_block.properties:
                props[prop] = java_block.properties[prop].value
              print(f'Warning: {java_block}{json.dumps(props)} is not mapped to anything. It will be replaced by air.')
              continue

            # Check if the block has a data value
            if len(mapped_block['dungeons']) > 1:
              tile.set_block(tx, ty, tz, block_id = mapped_block['dungeons'][0], block_data = mapped_block['dungeons'][1])
            else:
              tile.set_block(tx, ty, tz, block_id = mapped_block['dungeons'][0])

      # Convert plane images to tile planes
      if os.path.isfile(os.path.join(self.world_dir, 'region_plane', tile.id + '.png')):
        img = Image.open(os.path.join(self.world_dir, 'region_plane', tile.id + '.png')).convert('RGB')
        for x in range(tile.size[0]):
          for z in zi:
            pixel = img.getpixel((x, z))
            idx = tile.get_block_index(x, 0, z)
            if pixel in region_plane_colors:
              tile.region_plane[idx] = region_plane_colors.index(pixel)
            else:
              tile.region_plane[idx] = region_plane_colors.index(closest_color(pixel, region_plane_colors))

      if os.path.isfile(os.path.join(self.world_dir, 'region_y_plane', tile.id + '.png')):
        tile.region_y_plane_copy_height = False
        img = Image.open(os.path.join(self.world_dir, 'region_y_plane', tile.id + '.png')).convert('L')
        for x in range(tile.size[0]):
          for z in zi:
            idx = tile.get_block_index(x, 0, z)
            tile.region_y_plane[idx] = img.getpixel((x, z))

      if os.path.isfile(os.path.join(self.world_dir, 'walkable_plane', tile.id + '.png')):
        tile.write_walkable_plane = True
        img = Image.open(os.path.join(self.world_dir, 'walkable_plane', tile.id + '.png')).convert('L')
        for x in range(tile.size[0]):
          for z in zi:
            idx = tile.get_block_index(x, 0, z)
            tile.walkable_plane[idx] = img.getpixel((x, z))

    if dict_format:
      return {'objects':[t.dict() for t in tiles]}
    else:
      return {'objects':tiles}


class ObjectGroupToJavaWorld:
  """Converter that takes a Dungeons object group and creates a Java Edition world."""
  def __init__(self, objectgroup, world_dir, resources_pack_path=None):
    self.objectgroup = objectgroup
    self.world_dir = world_dir
    self.level_name = 'Converted Object Group'
    self.boundary_block = anvil.Block('minecraft', 'barrier')

    # If Not None, it will convert a MC Dungeon resources pack to a MC resources pack
    self.resources_pack_path = resources_pack_path

    # If True, convert regions that are small enough to structure blocks
    self.region_structure_blocks = True

    # If True, use player heads as playerstart regions instead of structure blocks
    self.playerstart_to_player_head = True

  def convert(self):
    """Creates a Java Edition world in the world directory from the object group."""
    # TODO: Converting to a Java world should be done one region or maybe even
    # one sub-region at a time. Right now, all regions are kept
    # in memory until the conversion process is done, which means the memory
    # usage can be massive for bigger object groups.

    # anvil-parser doesn't actually support loading a region from a file and
    # then editing it and writing it to a file again. Regions loaded from a
    # file are read-only, and the regions that can be edited start out empty.

    region_cache = {}
    block_cache = {}

    def get_region(rx, rz):
      if f'{rx}x{rz}' in region_cache:
        return region_cache[f'{rx}x{rz}']
      else:
        region_cache[f'{rx}x{rz}'] = anvil.EmptyRegion(rx, rz)
        return region_cache[f'{rx}x{rz}']

    structure_block = anvil.Block('minecraft', 'structure_block')
    player_head = anvil.Block('minecraft', 'player_head')

    def find_room_for_structure_block(area, get_block):
      xi = range(area[0])
      zi = range(area[1])

      # Blocks that will break if a stucture block is placed on top of them
      breakable_blocks = [0x3c, 0xc6]

      # Check the area and blocks above it
      for y in range(49):
        for x in xi:
          for z in zi:
            if get_block(x, y, z) == 0 and not get_block(x, y - 1, z) in breakable_blocks:
              return (x, y, z)

      # Check blocks below the area
      for y in range(-1, -49, -1):
        for x in xi:
          for z in zi:
            if get_block(x, y, z) == 0 and not get_block(x, y - 1, z) in breakable_blocks:
              return (x, y, z)

      # No room found :(
      return None

    if isinstance(self.objectgroup, dict):
      og = self.objectgroup

    else: # If objectgroup is a file path, parse the json file
      with open(self.objectgroup) as json_file:
        og = json.load(json_file)

    os.makedirs(os.path.join(self.world_dir, 'region_plane'), exist_ok=True)
    os.makedirs(os.path.join(self.world_dir, 'region_y_plane'), exist_ok=True)
    os.makedirs(os.path.join(self.world_dir, 'walkable_plane'), exist_ok=True)

    for tile_dict in og['objects']:
      if isinstance(tile_dict, Tile):
        tile = tile_dict
      else:
        tile = Tile.from_dict(tile_dict)

      zi = range(tile.size[2])
      yi = range(min(256, tile.size[1]))

      # For each slice of the tile along the X axis...
      for tx in range(tile.size[0]):
        ax = tx + tile.pos[0]
        rx = ax // 512

        # For each column of the slice along the Z axis...
        for tz in zi:
          az = tz + tile.pos[2]
          rz = az // 512
          region = get_region(rx, rz)

          # For each block in the column along the Y axis...
          for ty in yi:
            ay = ty + tile.pos[1]

            # Skip this block if it's outside of the world bounds
            if ay < 0 or ay >= 256:
              continue

            bidx = tile.get_block_index(tx, ty, tz)

            # If the block is just air, we don't need to do anything
            if tile.blocks[bidx] == 0:
              continue

            # Get the Java block from the cache if it's there
            bcid = tile.blocks[bidx] << 4 | tile.block_data[bidx]
            if bcid in block_cache:
              java_block = block_cache[bcid]

            else: # If not, find it and add it to the cache to speed things up later
              mapped_block = find_dungeons_block(tile.blocks[bidx], tile.block_data[bidx])

              if mapped_block is None:
                print(f'Warning: {tile.blocks[bidx]}:{tile.block_data[bidx]} is not mapped to anything. It will be replaced by air.')
                continue

              if len(mapped_block['java']) > 1:
                java_block = anvil.Block(*mapped_block['java'][0].split(':', 1), mapped_block['java'][1])
              else:
                java_block = anvil.Block(*mapped_block['java'][0].split(':', 1))

              block_cache[bcid] = java_block

            # Once we have the Java block, add it to the region
            region.set_block(java_block, ax, ay, az)

      # TODO: Block post-processing to fix fences, walls, stairs, and more

      converter_blocks = []

      # Add the tile doors to the world
      for door in tile.doors:
        def get_block(x, y, z):
          tx = x + door.pos[0]
          ty = y + door.pos[1]
          tz = z + door.pos[2]
          if f'{tx},{ty},{tz}' in converter_blocks:
            return -1
          if tx >= 0 and tx < tile.size[0] and ty >= 0 and ty < tile.size[1] and tz >= 0 and tz < tile.size[2]:
            return tile.get_block_id(tx, ty, tz)
          else:
            return 0
        pos = find_room_for_structure_block(door.size[::2], get_block)

        if pos is None:
          if hasattr(door, 'name'):
            print(f'Warning: No room to place structure block for door: {door.name}')
          else:
            print(f'Warning: No room to place structure block for unnamed door.')

        else:
          tpos = [p + d for p, d in zip(pos, door.pos)]
          if tpos[0] >= 0 and tpos[0] < tile.size[0] and tpos[1] >= 0 and tpos[1] < tile.size[1] and tpos[2] >= 0 and tpos[2] < tile.size[2]:
            apos = [p + t for p, t in zip(tpos, tile.pos)]
            region = get_region(apos[0] // 512, apos[2] // 512)
            region.set_block(structure_block, *apos)
            metadata = door.dict()
            metadata.pop('name', None)
            metadata.pop('pos', None)
            metadata.pop('size', None)
            if hasattr(door, 'name'):
              tile_entity = structure_block_entity(*apos, 'SAVE', f'door:{door.name}', json.dumps(metadata), *[-v for v in pos], *door.size)
            else:
              tile_entity = structure_block_entity(*apos, 'SAVE', 'door:', json.dumps(metadata), *[-v for v in pos], *door.size)
            region.chunks[apos[2] // 16 % 32 * 32 + apos[0] // 16 % 32].tile_entities.append(tile_entity)
            converter_blocks.append(f'{tpos[0]},{tpos[1]},{tpos[2]}')

      if self.region_structure_blocks:
        # Add the tile regions to the world
        for tile_region in tile.regions:
          # playerstart regions just use a player head instead of a structure block
          if self.playerstart_to_player_head and hasattr(tile_region, 'tags') and tile_region.tags == 'playerstart':
            ax = tile.pos[0] + tile_region.pos[0]
            ay = tile.pos[1] + tile_region.pos[1]
            az = tile.pos[2] + tile_region.pos[2]
            rx = ax // 512
            rz = az // 512
            region = get_region(rx, rz)
            region.set_block(player_head, ax, ay, az)
            tile_entity = TAG_Compound()
            tile_entity.tags.extend([
              TAG_String(name='id', value='minecraft:skull'),
              TAG_Byte(name='keepPacked', value=0),
              TAG_Int(name='x', value=ax),
              TAG_Int(name='y', value=ay),
              TAG_Int(name='z', value=az)
            ])
            region.chunks[az // 16 % 32 * 32 + ax // 16 % 32].tile_entities.append(tile_entity)
            converter_blocks.append(f'{tile_region.pos[0]},{tile_region.pos[1]},{tile_region.pos[2]}')

          elif tile_region.size[0] <= 48 and tile_region.size[1] <= 48 and tile_region.size[2] <= 48:
            def get_block(x, y, z):
              tx = x + tile_region.pos[0]
              ty = y + tile_region.pos[1]
              tz = z + tile_region.pos[2]
              if f'{tx},{ty},{tz}' in converter_blocks:
                return -1
              if tx >= 0 and tx < tile.size[0] and ty >= 0 and ty < tile.size[1] and tz >= 0 and tz < tile.size[2]:
                return tile.get_block_id(tx, ty, tz)
              else:
                return 0
            pos = find_room_for_structure_block(tile_region.size[::2], get_block)

            if pos is None:
              if hasattr(tile_region, 'name'):
                print(f'Warning: No room to place structure block for region: {tile_region.name}')
              else:
                print(f'Warning: No room to place structure block for unnamed region.')

            else:
              tpos = [p + d for p, d in zip(pos, tile_region.pos)]
              if tpos[0] >= 0 and tpos[0] < tile.size[0] and tpos[1] >= 0 and tpos[1] < tile.size[1] and tpos[2] >= 0 and tpos[2] < tile.size[2]:
                apos = [p + t for p, t in zip(tpos, tile.pos)]
                region = get_region(apos[0] // 512, apos[2] // 512)
                region.set_block(structure_block, *apos)
                metadata = tile_region.dict()
                metadata.pop('name', None)
                metadata.pop('pos', None)
                metadata.pop('size', None)
                if hasattr(tile_region, 'name'):
                  tile_entity = structure_block_entity(*apos, 'SAVE', f'region:{tile_region.name}', json.dumps(metadata), *[-v for v in pos], *tile_region.size)
                else:
                  tile_entity = structure_block_entity(*apos, 'SAVE', 'region:', json.dumps(metadata), *[-v for v in pos], *tile_region.size)
                region.chunks[apos[2] // 16 % 32 * 32 + apos[0] // 16 % 32].tile_entities.append(tile_entity)
                converter_blocks.append(f'{tpos[0]},{tpos[1]},{tpos[2]}')

      # Add the tile boundaries to the world
      for boundary in tile.boundaries:
        ax = tile.pos[0] + boundary.x
        az = tile.pos[2] + boundary.z
        rx = ax // 512
        rz = az // 512
        region = get_region(rx, rz)

        for by in range(boundary.h):
          ay = tile.pos[1] + boundary.y + by

          region.set_block(self.boundary_block, ax, ay, az)

      # Convert the planes to images, so they can be edited easily
      region_plane_img = Image.new('RGB', (tile.size[0], tile.size[2]))
      region_y_plane_img = Image.new('L', (tile.size[0], tile.size[2]))
      walkable_plane_img = Image.new('L', (tile.size[0], tile.size[2]))
      for x in range(tile.size[0]):
        for z in zi:
          idx = tile.get_block_index(x, 0, z)
          region_plane_img.putpixel((x, z), region_plane_colors[tile.region_plane[idx]])
          region_y_plane_img.putpixel((x, z), tile.region_y_plane[idx])
          walkable_plane_img.putpixel((x, z), tile.walkable_plane[idx])

      region_plane_img.save(os.path.join(self.world_dir, 'region_plane', tile.id + '.png'))
      region_y_plane_img.save(os.path.join(self.world_dir, 'region_y_plane', tile.id + '.png'))
      walkable_plane_img.save(os.path.join(self.world_dir, 'walkable_plane', tile.id + '.png'))

    with open(os.path.join(self.world_dir, 'region_plane', '_README.txt'), 'w') as region_plane_readme:
      region_plane_readme.write('Region plane colors:\n\n')
      region_plane_readme.write('\n'.join([('#%02x%02x%02x' % c) + f': {n}' for c, n in zip(region_plane_colors, region_plane_color_names)]))

    # Write regions to files
    os.makedirs(os.path.join(self.world_dir, 'region'), exist_ok=True)
    for k in region_cache:
      region_cache[k].save(os.path.join(self.world_dir, f'region/r.{region_cache[k].x}.{region_cache[k].z}.mca'))

    # For convenience, write the object group to objectgroup.json in the world
    # directory, so JavaWorldToObjectGroup can convert the world back to an
    # object group without any changes.
    og_copy = json.loads(json.dumps(og)) # faster than copy.deepcopy
    for tile in og_copy['objects']:
      tile.pop('blocks', None)
      tile.pop('boundaries', None)
      tile.pop('doors', None)
      tile.pop('height-plane', None)
      tile.pop('region-plane', None)
      tile.pop('region-y-plane', None)
      tile.pop('walkable-plane', None)
      if self.region_structure_blocks and 'regions' in tile:
        # Keep only regions that are too big turn into structure blocks
        tile['regions'] = [r for r in tile['regions'] if r['size'][0] > 48 or r['size'][1] > 48 or r['size'][2] > 48]
    with open(os.path.join(self.world_dir, 'objectgroup.json'), 'w') as out_file:
      out_file.write(stringify(og_copy))

    # Create level.dat file
    level = NBTFile('level_template.dat', 'rb')
    level['Data']['LevelName'].value = self.level_name
    level['Data']['LastPlayed'].value = int(time.time()*1000)

    # Place the player spawn above the center of the first tile.
    # This could probably be made a bit smarter, since the center of the tile
    # might still be above the void. For now, this faster solution will have to do.
    level['Data']['SpawnX'].value = int(og['objects'][0]['pos'][0] + og['objects'][0]['size'][0] * 0.5)
    level['Data']['SpawnY'].value = min(255, og['objects'][0]['pos'][1] + og['objects'][0]['size'][1])
    level['Data']['SpawnZ'].value = int(og['objects'][0]['pos'][2] + og['objects'][0]['size'][2] * 0.5)

    level.write_file(os.path.join(self.world_dir, 'level.dat'))

    if self.resources_pack_path is not None:
      print("Resource pack")
      DungeonToJavaResourcesPack(resource_pack_path=self.resources_pack_path,
                                 dest_path=os.path.join(self.world_dir, "resources"),
                                 verbose=False).convert()