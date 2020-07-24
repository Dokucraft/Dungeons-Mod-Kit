@echo off
SET "ddp=%~dp0"
SET "ddp=%ddp:~0,-1%"

SET /p editorPath= < Tools\user_settings\editor_directory.txt

python Tools\py\generate_asset_import_settings.py
"%editorPath%\UE4Editor-Cmd.exe" "%ddp%\UE4Project\Dungeons.uproject" -run=ImportAssets -nosourcecontrol "-importsettings=%ddp%\Tools\tmp_import_settings.json"

del /s Tools\tmp_import_settings.json  >nul 2>&1