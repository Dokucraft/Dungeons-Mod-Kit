import os
import json
import math

texturesPath = '../Block Textures/'

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

count = 0
redundant_files_message_shown = False

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  for filename,copies in textures.items():
    if not os.path.isfile(texturesPath + filename):
      count += 1
      print(filename)

  total = len(textures)
  print()
  print('----------------------------------------')
  print('  Total missing: ' + str(count))
  print('  Total done:    ' + str(total - count))
  print('  Complete:      ' + str(math.floor((total - count) * 100 / total)) + '%')
  print('----------------------------------------')

  for f in [f.path.replace('\\', '/').replace(texturesPath, '') for f in scantree(texturesPath)]:
    if not f in textures:
      if not redundant_files_message_shown:
        print()
        print('! Redundant files detected:')
        redundant_files_message_shown = True
      print(f)

print()