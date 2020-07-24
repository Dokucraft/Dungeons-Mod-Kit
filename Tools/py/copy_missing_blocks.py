import os
import json
import shutil
import sys

texturesPath = '../Block Textures/'
outputDir = '../Missing Textures/'

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  for filename,copies in textures.items():
    if os.path.isfile(texturesPath + filename):
      print('Skipping ' + texturesPath + filename + '...')
    else:
      print('Copying ' + texturesPath + filename + '...')
      os.makedirs(os.path.dirname(outputDir), exist_ok=True)
      shutil.copyfile(sys.argv[1] + '/Dungeons/Content/data/resourcepacks/' + copies[0], outputDir + filename)