import os
import json
import math

blockTexturesPath = '../Block Textures/'
unrealTexturesPath = '../UE4Project/Content/'

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

blocksCount = 0
unrealCount = 0
totalBlocks = None
totalUnreal = None
redundant_files_message_shown = False

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  totalBlocks = len(textures)
  for filename,copies in textures.items():
    if not os.path.isfile(blockTexturesPath + filename):
      blocksCount += 1

with open('configs/actors_prefabs_list.json') as json_file:
  textures = json.load(json_file)
  totalUnreal = len(textures)
  for filename in textures:
    if not os.path.isfile(unrealTexturesPath + filename):
      unrealCount += 1

print()
print('------------------------------------------------')
print('  Missing blocks:              ' + str(blocksCount))
print('  Blocks done:                 ' + str(totalBlocks - blocksCount))
print('  Complete blocks:             ' + str(math.floor((totalBlocks - blocksCount) * 100 / totalBlocks)) + '%')
print()
print('  Missing actors and prefabs:  ' + str(unrealCount))
print('  Actors and prefabs done:     ' + str(totalUnreal - unrealCount))
print('  Complete actors and prefabs: ' + str(math.floor((totalUnreal - unrealCount) * 100 / totalUnreal)) + '%')
print()
print('  Total missing:               ' + str(blocksCount + unrealCount))
print('  Total done:                  ' + str(totalBlocks + totalUnreal - blocksCount - unrealCount))
print('  Complete:                    ' + str(math.floor((totalBlocks + totalUnreal - blocksCount - unrealCount) * 100 / (totalBlocks + totalUnreal))) + '%')
print('------------------------------------------------')
print()