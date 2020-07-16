@echo off
RD /q /s "..\Missing Textures" > nul 2> nul
SET /p quickbmsExportDir= < settings\quickbms_export_dir.txt
python copy_missing_blocks.py "%quickbmsExportDir:\=/%"