SET "ddp=%~dp0"
SET "ddp=%ddp:~0,-1%"

SET /p editorPath= < Tools\settings\editor_directory.txt

del /S Dungeons\*.uasset
del /S Dungeons\*.ubulk
del /S Dungeons\*.uexp

"%editorPath%\UE4Editor-Cmd.exe" "%ddp%\UE4Project\Dungeons.uproject" -run=cook -targetplatform=WindowsNoEditor

robocopy /job:Tools\copy_cooked_assets