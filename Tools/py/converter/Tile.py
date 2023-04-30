import zlib
import base64
from array import array
from itertools import chain, zip_longest

"""
This module contains useful classes for different tile-related objects.

The documentation here isn't great, but hopefully most of the function names
are self-explanatory.

There are still some parts that aren't implemented yet and parts that could be
optimized better.
"""

def decompress(s):
  return zlib.decompress(base64.b64decode(s))

def compress(b):
  return base64.b64encode(zlib.compress(b, 9)).decode('utf-8')

def pairwise(iterable):
  "s -> (s0, s1), (s2, s3), (s4, s5), ..."
  a = iter(iterable)
  return zip(a, a)


class Boundary:
  """
  Tile boundary, which is a column of invisible, solid blocks.
  Boundaries only have solid walls; the top and bottom are not solid.
  """
  def __init__(self, x, y, z, h):
    self.x = x
    self.y = y
    self.z = z
    self.h = h

  @staticmethod
  def from_bytes(bytes_):
    """Returns a Boundary object with properties from the given bytes."""
    return Boundary(
      x = bytes_[0] << 8 | bytes_[1],
      y = bytes_[2] << 8 | bytes_[3],
      z = bytes_[4] << 8 | bytes_[5],
      h = bytes_[6] << 8 | bytes_[7])

  def bytes(self):
    """Returns the boundary represented as bytes."""
    return bytes([
      self.x >> 8 & 0xff, self.x & 0xff,
      self.y >> 8 & 0xff, self.y & 0xff,
      self.z >> 8 & 0xff, self.z & 0xff,
      self.h >> 8 & 0xff, self.h & 0xff])


class Door:
  """
  Tile door, which is a tile connection or teleport point.
  """
  def __init__(self, pos = [0, 0, 0], size = [1, 1, 1]):
    self.pos = pos
    self.size = size

  @staticmethod
  def from_dict(dict_door):
    """Returns a Door object with properties from the given dict."""
    door = Door(dict_door['pos'], dict_door['size'])

    if 'name' in dict_door:
      door.name = dict_door['name']

    if 'tags' in dict_door:
      door.tags = dict_door['tags']

    return door

  def dict(self):
    """Returns the door represented as a dict."""
    dict = {}

    if hasattr(self, 'name'):
      dict['name'] = self.name

    if hasattr(self, 'tags'):
      dict['tags'] = self.tags

    dict['pos'] = self.pos
    dict['size'] = self.size

    return dict


class Region:
  """
  Tile region, which is an area marker that can be used set up triggers
  or place objects in the level.

  Not yet implemented:
  - 'locked' property
  """
  def __init__(self, pos = [0, 0, 0], size = [1, 1, 1]):
    self.pos = pos
    self.size = size

  @staticmethod
  def from_dict(dict_region):
    """Returns a Region object with properties from the given dict."""
    region = Region(dict_region['pos'], dict_region['size'])

    if 'name' in dict_region:
      region.name = dict_region['name']

    if 'tags' in dict_region:
      region.tags = dict_region['tags']

    if 'type' in dict_region:
      region.type = dict_region['type']

    return region

  def dict(self):
    """Returns the region represented as a dict."""
    dict = {}

    if hasattr(self, 'name'):
      dict['name'] = self.name

    if hasattr(self, 'tags'):
      dict['tags'] = self.tags

    if hasattr(self, 'type'):
      dict['type'] = self.type

    dict['pos'] = self.pos
    dict['size'] = self.size

    return dict


class Tile:
  """
  A tile is a cuboid chunk of blocks. They are pieced together to create
  the levels in Dungeons.

  Not yet implemented:
  - 'is-leaky' property
  - 'locked' property
  - 'tags' property
  """
  def __init__(self, name, size):
    self.id = name
    self.size = size
    self.volume = size[0] * size[1] * size[2]
    self.blocks = array('H', [0] * self.volume) # unsigned 16-bit int array
    self.block_data = bytearray([0] * self.volume)
    self.region_plane = bytearray([0] * (size[0] * size[2]))
    self.region_y_plane = bytearray([0] * (size[0] * size[2]))
    self.region_y_plane_copy_height = True
    self.walkable_plane = bytearray([0] * (size[0] * size[2]))
    self.write_walkable_plane = False
    self.y = 0
    self.pos = None
    self.boundaries = []
    self.doors = []
    self.regions = []

  @staticmethod
  def from_dict(dict_tile):
    """Returns a Tile object with properties from the given dict."""
    if 'size' in dict_tile:
      tile = Tile(dict_tile['id'], dict_tile['size'])

      if 'pos' in dict_tile:
        tile.pos = dict_tile['pos']

    elif 'pos' in dict_tile and 'pos2' in dict_tile:
      tile = Tile(dict_tile['id'], [abs(a-b) + 1 for a, b in zip(dict_tile['pos'], dict_tile['pos2'])])
      tile.pos = [min(a, b) for a, b in zip(dict_tile['pos'], dict_tile['pos2'])]
    else:
      raise Exception('Tile is missing the size property.')

    if 'blocks' in dict_tile:
      decompressed_blocks = decompress(dict_tile['blocks'])

      # If the number of bytes is greater than 2 times the tile volume, the tile must be using the 16-bit format
      if len(decompressed_blocks) > tile.volume * 2:
        # IDs are the first {tile.volume} 16-bit ints
        tile.blocks = array('H', [x[0] << 8 | x[1] for x in pairwise(decompressed_blocks[:tile.volume*2])])
        # Data values are only 4 bits each, so we need to split each byte in 2 and create a 1D list from that
        tile.block_data = bytearray(chain.from_iterable([(d >> 4, d & 0xf) for d in decompressed_blocks[tile.volume*2:]]))
      else:
        # IDs are simply the first {tile.volume} bytes
        tile.blocks = array('H', iter(decompressed_blocks[:tile.volume]))
        # Data values are only 4 bits each, so we need to split each byte in 2 and create a 1D list from that
        tile.block_data = bytearray(chain.from_iterable([(d >> 4, d & 0xf) for d in decompressed_blocks[tile.volume:]]))

    if 'region-plane' in dict_tile:
      tile.region_plane = bytearray(decompress(dict_tile['region-plane']))

    if 'region-y-plane' in dict_tile:
      tile.region_y_plane = bytearray(decompress(dict_tile['region-y-plane']))
      tile.region_y_plane_copy_height = False

    if 'walkable-plane' in dict_tile:
      tile.walkable_plane = bytearray(decompress(dict_tile['walkable-plane']))
      tile.write_walkable_plane = True

    if 'y' in dict_tile:
      tile.y = dict_tile['y']

    if 'doors' in dict_tile:
      tile.doors = [Door.from_dict(d) for d in dict_tile['doors']]

    if 'regions' in dict_tile:
      tile.regions = [Region.from_dict(r) for r in dict_tile['regions']]

    if 'boundaries' in dict_tile:
      # Old uncompressed boundaries format
      if isinstance(dict_tile['boundaries'], list):
        tile.boundaries = [Boundary(*b) for b in dict_tile['boundaries']]

      else: # Normal compressed format
        boundaries_bytes = decompress(dict_tile['boundaries'])
        for i in range(0, len(boundaries_bytes), 8):
          tile.boundaries.append(Boundary.from_bytes(boundaries_bytes[i:i+8]))

    return tile

  def dict(self):
    """Returns the tile represented as a dict.

    The height-plane property is automatically generated.
    """
    obj = {
      'id': self.id,
      'size': self.size
    }

    if self.pos != None:
      obj['pos'] = self.pos

    if any([x > 0xff for x in self.blocks]): # Requires 16-bit format
      obj['blocks'] = compress(
        bytearray(chain.from_iterable([(x >> 8, x & 0xff) for x in self.blocks])) +
        bytearray([a << 4 | b & 0xf for a, b in zip_longest(self.block_data[::2], self.block_data[1::2], fillvalue=0)])
      )
    else: # Can use 8-bit format
      obj['blocks'] = compress(
        bytearray(tuple(self.blocks)) +
        bytearray([a << 4 | b & 0xf for a, b in zip_longest(self.block_data[::2], self.block_data[1::2], fillvalue=0)])
      )
    obj['region-plane'] = compress(self.region_plane)
    obj['height-plane'] = compress(bytes(self.get_height_map()))

    if self.region_y_plane_copy_height:
      obj['region-y-plane'] = obj['height-plane']
    else:
      obj['region-y-plane'] = compress(self.region_y_plane)

    if self.write_walkable_plane:
      obj['walkable-plane'] = compress(self.walkable_plane)

    if len(self.boundaries) > 0:
      boundaries = bytearray()
      for boundary in self.boundaries:
        boundaries.extend(boundary.bytes())
      obj['boundaries'] = compress(boundaries)

    if self.y != 0:
      obj['y'] = self.y

    if len(self.doors) > 0:
      obj['doors'] = [d.dict() for d in self.doors]

    if len(self.regions) > 0:
      obj['regions'] = [r.dict() for r in self.regions]

    return obj

  def resize(self, x, y, z):
    """Resizes the tile to the given size.

    Anything that is dependant on the tile's size is reset.
    """
    self.size = [x, y, z]
    self.volume = x * y * z
    self.blocks = array('H', [0] * self.volume)
    self.block_data = bytearray([0] * self.volume)
    self.region_plane = bytearray([0] * (x * z))
    self.region_y_plane = bytearray([0] * (x * z))

  def get_block_index(self, x, y, z):
    """Returns the index of the block at the given position.

    This function is useful if you need to get both the block ID and data value
    at the same time. get_block_id and get_block_data are more convenient, but
    when iterating over all blocks in the tile, using this will be faster."""

    return (y * self.size[2] + z) * self.size[0] + x

  def get_block_id(self, x, y, z):
    """Returns the ID of the block at the given position."""

    # We could use self.get_block_index(x, y, z) here, but this is faster
    return self.blocks[(y * self.size[2] + z) * self.size[0] + x]

  def get_block_data(self, x, y, z):
    """Returns the data value of the block at the given position."""

    # We could use self.get_block_index(x, y, z) here, but this is faster
    return self.block_data[(y * self.size[2] + z) * self.size[0] + x]

  def set_block(self, x, y, z, block_id, block_data = 0):
    """Sets the block at the given position to the given block ID and data value."""

    idx = (y * self.size[2] + z) * self.size[0] + x
    self.blocks[idx] = block_id
    self.block_data[idx] = block_data

  def get_region_value(self, x, z):
    """Returns the value of the region plane at the given position."""

    return self.region_plane[z * self.size[0] + x]

  def set_region_value(self, x, z, value):
    """Sets the value of the region plane at the given position to the given value."""

    self.region_plane[z * self.size[0] + x] = value

  def get_region_y_value(self, x, z):
    """Returns the value of the region-y plane at the given position."""

    return self.region_y_plane[z * self.size[0] + x]

  def set_region_y_value(self, x, z, value):
    """Sets the value of the region-y plane at the given position to the given value."""

    self.region_y_plane[z * self.size[0] + x] = value

  def get_height_map(self):
    """Returns a height map of the tile as a 1D list."""

    zr = range(0, self.size[2])
    yr = range(min(self.size[1] - 1, 254), -1, -1)
    height_map = [0] * (self.size[0] * self.size[2])
    for x in range(0, self.size[0]):
      for z in zr: # zr and yr are created only once above to save time
        for y in yr: # Start at the top and go down until a solid block is found
          if self.get_block_id(x, y, z) != 0: # Block is not air
            height_map[z * self.size[0] + x] = y + 1
            break
    return height_map