import os
import json
import math

texturesPath = '../Block Textures/'

count = 0

with open('block_textures.json') as json_file:
  textures = json.load(json_file)
  for filename,copies in textures.items():
    if not os.path.isfile(texturesPath + filename):
      count += 1
      print(filename)

  total = len(textures)
  print('----------------------------------------')
  print('  Total missing: ' + str(count))
  print('  Complete:      ' + str(math.floor((total - count) * 100 / total)) + '%')
  print('----------------------------------------')