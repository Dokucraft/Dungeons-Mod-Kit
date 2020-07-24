import os
import json

texturesPath = '../Block Textures/'

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

with open('configs/block_textures.json') as json_file:
  textures = json.load(json_file)
  for f in [f.path.replace('\\', '/') for f in scantree(texturesPath)]:
    if not f.replace(texturesPath, '') in textures:
      print('Deleting ' + f)
      os.remove(f)