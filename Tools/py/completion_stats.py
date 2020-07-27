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
equipmentsCount = 0
itemsCount = 0
mobsCount = 0
prefabsCount = 0
totalBlocks = None
totalEquipments = None
totalItems = None
totalMobs = None
totalPrefabs = None
redundant_files_message_shown = False

os.system('chcp 65001')
os.system('cls')

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  totalBlocks = len(textures)
  for filename,copies in textures.items():
    if not os.path.isfile(blockTexturesPath + filename):
      blocksCount += 1

with open('configs/equipments_list.json') as json_file:
  textures = json.load(json_file)
  totalEquipments = len(textures)
  for filename in textures:
    if not os.path.isfile(unrealTexturesPath + filename):
      equipmentsCount += 1

with open('configs/items_list.json') as json_file:
  textures = json.load(json_file)
  totalItems = len(textures)
  for filename in textures:
    if not os.path.isfile(unrealTexturesPath + filename):
      itemsCount += 1

with open('configs/mobs_list.json') as json_file:
  textures = json.load(json_file)
  totalMobs = len(textures)
  for filename in textures:
    if not os.path.isfile(unrealTexturesPath + filename):
      mobsCount += 1

with open('configs/prefabs_list.json') as json_file:
  textures = json.load(json_file)
  totalPrefabs = len(textures)
  for filename in textures:
    if not os.path.isfile(unrealTexturesPath + filename):
      prefabsCount += 1

print('\x1b[1m')
print('────────────────────────────────────────────────')
print('  Blocks     :')
print('     - Total    : ' + str(totalBlocks))
print('     -\x1b[31m Missing \x1b[37m : ' + str(blocksCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalBlocks - blocksCount) + ' (' + str(math.floor((totalBlocks - blocksCount) * 100 / totalBlocks)) + '%)' )

print()

print('  Equipments :')
print('     - Total    : ' + str(totalEquipments))
print('     -\x1b[31m Missing \x1b[37m : ' + str(equipmentsCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalEquipments - equipmentsCount) + ' (' + str(math.floor((totalEquipments - equipmentsCount) * 100 / totalEquipments)) + '%)' )

print()

print('  Items      :')
print('     - Total    : ' + str(totalItems))
print('     -\x1b[31m Missing \x1b[37m : ' + str(itemsCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalItems - itemsCount) + ' (' + str(math.floor((totalItems - itemsCount) * 100 / totalItems)) + '%)' )

print()

print('  Mobs       :')
print('     - Total    : ' + str(totalMobs))
print('     -\x1b[31m Missing \x1b[37m : ' + str(mobsCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalMobs - mobsCount) + ' (' + str(math.floor((totalMobs - mobsCount) * 100 / totalMobs)) + '%)' )

print()

print('  Prefabs    :')
print('     - Total    : ' + str(totalPrefabs))
print('     -\x1b[31m Missing \x1b[37m : ' + str(prefabsCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalPrefabs - prefabsCount) + ' (' + str(math.floor((totalPrefabs - prefabsCount) * 100 / totalPrefabs)) + '%)' )

print()

totalGlobal = totalEquipments + totalBlocks + totalItems + totalMobs + totalPrefabs
globalCount = equipmentsCount + blocksCount + itemsCount + mobsCount + prefabsCount

print('  Global     :')
print('     - Total    : ' + str(totalGlobal))
print('     -\x1b[31m Missing \x1b[37m : ' + str(globalCount))
print('     -\x1b[32m Done    \x1b[37m : ' + str(totalGlobal - globalCount) + ' (' + str(math.floor((totalGlobal - globalCount) * 100 / (totalGlobal))) + '%)' )
print('────────────────────────────────────────────────')

print()