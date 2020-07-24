@echo off
RD /q /s "..\Missing Textures" > nul 2> nul
SET /p quickbmsExportDir= < user_settings\quickbms_export_dir.txt
python py\copy_missing_blocks.py "%quickbmsExportDir:\=/%"