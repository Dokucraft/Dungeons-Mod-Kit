@echo off
echo Are you sure you want to delete the redundant files in Block Textures? (yes/no)
SET /P CONFIRMPROMPT= ^> 
IF /I "%CONFIRMPROMPT%" NEQ "yes" GOTO EOF

python py\delete_redundant_block_textures.py
pause