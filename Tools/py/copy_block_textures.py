import os
import json
import shutil

texturesPath = '../Block Textures/'
outputDir = '../Dungeons/Content/data/resourcepacks/'

os.makedirs(outputDir, exist_ok=True)

for packDir in [f.path for f in os.scandir(outputDir) if f.is_dir()]:
  os.makedirs(packDir + '/images/blocks', exist_ok=True)
  for filePath in [f.path for f in os.scandir(packDir + '/images/blocks') if f.is_file() and f.name.endswith('.png')]:
    print('Deleting ' + filePath + '...')
    os.remove(filePath)

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  for filename,copies in textures.items():
    if os.path.isfile(texturesPath + filename):
      print('Copying ' + texturesPath + filename + '...')
      for copy in copies:
        os.makedirs(os.path.dirname(outputDir + copy), exist_ok=True)
        shutil.copyfile(texturesPath + filename, outputDir + copy)