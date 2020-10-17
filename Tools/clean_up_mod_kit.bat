@echo off
echo.
echo Are you absolutely sure you want to delete all mod files in the mod kit? (yes/no)
echo Restoring the files might be impossible. Make a backup of the mod kit folder if you are unsure.
SET /P CONFIRMPROMPT= ^> 
IF /I "%CONFIRMPROMPT%" NEQ "yes" GOTO EOF

RD /q /s "..\Block Textures" > nul 2> nul
RD /q /s "..\Dungeons" > nul 2> nul
RD /q /s "..\UE4Project\Content" > nul 2> nul
RD /q /s "..\Precooked" > nul 2> nul

MD "..\Block Textures" > nul 2> nul
MD "..\Dungeons" > nul 2> nul
MD "..\UE4Project\Content" > nul 2> nul
MD "..\Precooked" > nul 2> nul