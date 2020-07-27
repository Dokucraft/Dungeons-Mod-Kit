import os
import json
import math

texturesPath = '../UE4Project/Content/'

def scantree(path):
  for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
      yield from scantree(entry.path)
    else:
      yield entry

count = 0
redundant_files_message_shown = False

os.system('chcp 65001')
os.system('cls')

print('────────────────────────────────────────────────')
print(' Show Missing & Present textures? ')
print(' - BOTH    : 1')
print(' - MISSING : 2')
print(' - PRESENT : 3')
print(' - ONLY %  : > 3 or < 1')

while True:
  try:
    ask = int(input("> "))
    break
  except ValueError:
    print('\x1b[1m \x1b[31m You have to enter a number! \x1b[0m')

with open('configs/mobs_list.json') as json_file:
  textures = json.load(json_file)
  for filename in textures:
    if os.path.isfile(texturesPath + filename) and ( ask == 1 or ask == 3):
      print('\x1b[1m \x1b[32m Present : ' + filename )
    if not os.path.isfile(texturesPath + filename):
      count += 1
      if ask == 2 or ask == 1 :
        print('\x1b[1m \x1b[31m Missing : ' + filename)

  total = len(textures)
  print('\x1b[0m \x1b[1m')
  print('────────────────────────────────────────────────')
  print('  Total : ' + str(total))
  print('    - \x1b[31m Missing \x1b[0m \x1b[1m : ' + str(count) )
  print('    - \x1b[32m Done    \x1b[0m \x1b[1m : ' + str(total - count) + ' (' + str(math.floor((total - count) * 100 / total)) + '%)')
  print('────────────────────────────────────────────────')

print()