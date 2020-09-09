import os
import hashlib
import unicodedata
import json
import re

from PIL import Image

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

def getHash(s):
  return hashlib.sha224(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')).hexdigest()

with open('user_settings/quickbms_export_dir.txt') as settings_file:
  quickbms_export_dir = settings_file.read().replace('\\', '/')

resourcepacks_dir = quickbms_export_dir + '/Dungeons/Content/data/resourcepacks'

# Group all identical textures together

hashes = {}

for png in [f.path.replace('\\', '/') for f in scantree(resourcepacks_dir) if f.name.endswith('.png') and '/images/blocks/' in f.path.replace('\\', '/')]:
  
  # Exclude some unneeded textures
  if (re.search('carried|reactor|camera|destroy_|build_|chest_| - Copy', png, flags=re.IGNORECASE)):
    continue

  # Get the hash of the pixel values instead of the file, since some textures are identical,
  # but for some reason have different metadata or compression
  img = Image.open(png).convert('RGBA')

  # Bitcrush the colors so very similar images end up in the same group
  # This can be done better, but this solution is very fast compared to other ones
  pixels = [v & 0xf0 for p in img.getdata() for v in p]

  h = getHash(str(pixels))

  if not h in hashes:
    hashes[h] = []

  hashes[h].append(png[len(resourcepacks_dir)+1:])

# While giving each group a file name, check if there is a similar group in the old config
# and reuse the name from that if there is. This makes the configs compatible so that
# a lot of the block textures don't have to be renamed

with open('configs/block_textures.json') as json_file:
  original = json.load(json_file)

compatible_config = {}

for h in hashes:
  similar = [k for k in original if not k in compatible_config and any(j in hashes[h] for j in original[k])]

  if len(similar) == 1:
    # If there is only one similar group, just use the name of that
    compatible_config[similar[0]] = hashes[h]

  elif len(similar) > 1:
    # If there are multiple similar groups, use the name of the most similar one
    counts = []
    for name in similar:
      counts.append((name, [k in hashes[h] for k in original[name]].count(True)))

    # This can be optimized, it doesn't have to sort the list, just find the item
    # with the largest number
    counts.sort(reverse=True, key=lambda x: x[1])
    compatible_config[counts[0][0]] = hashes[h]

  else:
    # If there are no similar groups, generate a new file name
    for p in hashes[h]:
      name = p.split('/')[-1]

      if not name in original and not name in compatible_config:
        compatible_config[name] = hashes[h]
        break

    else: # If none of the file names were available
      for p in hashes[h]:
        split = p.split('/')
        name = f'{split[-1][:-4]}_{split[0]}.png'

        if not name in original and not name in compatible_config:
          compatible_config[name] = hashes[h]
          break

      else: # If a file name still wasn't found, just add a number at the end
        base_name = hashes[h][0].split('/')[-1][:-4]
        i = 2
        name = f'{base_name}_{i}.png'
        while name in original or name in compatible_config:
          i += 1
          name = f'{base_name}_{i}.png'

        compatible_config[name] = hashes[h]

with open('configs/block_textures.json', 'w') as out_file:
  out_file.write(json.dumps(compatible_config, indent=2))