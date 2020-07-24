import os
import json

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

cwd = os.getcwd().replace('\\', '/')

importGroups = []

for png in [f.path.replace('\\', '/') for f in scantree('UE4Project/Content') if f.name.endswith('.png') and not os.path.isfile(os.path.splitext(f.path)[0]+'.uasset')]:
  group = {
    'GroupName': os.path.basename(png),
    'Filenames': [ cwd + '/' + png ],
    'DestinationPath': os.path.dirname(png).replace('UE4Project/Content', '/Game'),
    'bReplaceExisting':'true',
    'bSkipReadOnly':'false',
    'FactoryName': 'TextureFactory', 
    'ImportSettings': {
      'CompressionSettings': 'TC_BC7',
      'LODGroup': 'TEXTUREGROUP_Pixels2D'
    }
  }

  print('Importing ' + png.replace('UE4Project/Content/', ''))

  # Load custom import settings, if any
  if os.path.isfile(os.path.splitext(png)[0]+'.json'):
    with open(os.path.splitext(png)[0]+'.json') as json_file:
      for key,value in json.load(json_file).items():
        group['ImportSettings'][key] = value

  importGroups.append(group)

for fbx in [f.path.replace('\\', '/') for f in scantree('UE4Project/Content') if f.name.endswith('.fbx') and not os.path.isfile(os.path.splitext(f.path)[0]+'.uasset')]:
  group = {
    'GroupName': os.path.basename(fbx),
    'Filenames': [ cwd + '/' + fbx ],
    'DestinationPath': os.path.dirname(fbx).replace('UE4Project/Content', '/Game'),
    'bReplaceExisting':'true',
    'bSkipReadOnly':'false',
    'FactoryName': 'FbxFactory',
    'ImportSettings': {
      'bImportTextures': False,
      'bImportMaterials': True
    }
  }

  print('Importing ' + fbx.replace('UE4Project/Content/', ''))

  # Load custom import settings, if any
  if os.path.isfile(os.path.splitext(fbx)[0]+'.json'):
    with open(os.path.splitext(fbx)[0]+'.json') as json_file:
      for key,value in json.load(json_file).items():
        group['ImportSettings'][key] = value

  importGroups.append(group)

settingsFile = open('Tools/tmp_import_settings.json', 'w')
settingsFile.write(json.dumps({ 'ImportGroups': importGroups }))
settingsFile.close()