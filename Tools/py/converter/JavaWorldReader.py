from collections import OrderedDict
import anvil

"""Module for optimized reading of Minecraft Java Edition worlds.

Handles caching automatically.
"""

class JavaWorldReader:
  def __init__(self, world_dir):
    self.dir = world_dir

    self.region_cache_max = 4
    self.__region_cache = OrderedDict()

    self.chunk_cache_max = 64
    self.__chunk_cache = OrderedDict()

  def chunk(self, cx, cz):
    try:
      if f'{cx}x{cz}' in self.__chunk_cache:
        return self.__chunk_cache[f'{cx}x{cz}']

      else:
        rx = cx // 32
        rz = cz // 32

        if not f'{rx}x{rz}' in self.__region_cache:
          self.__region_cache[f'{rx}x{rz}'] = anvil.Region.from_file(f'{self.dir}/region/r.{rx}.{rz}.mca')
          if len(self.__region_cache) > self.region_cache_max:
            self.__region_cache.popitem(last=False)

        self.__chunk_cache[f'{cx}x{cz}'] = anvil.Chunk.from_region(self.__region_cache[f'{rx}x{rz}'], cx, cz)
        if len(self.__chunk_cache) > self.chunk_cache_max:
          self.__chunk_cache.popitem(last=False)
        return self.__chunk_cache[f'{cx}x{cz}']

    except:
      return None