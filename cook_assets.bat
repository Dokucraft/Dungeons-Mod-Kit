SET "ddp=%~dp0"
SET "ddp=%ddp:~0,-1%"

SET /p editorPath= < Tools\user_settings\editor_directory.txt

del /S Dungeons\*.uasset
del /S Dungeons\*.ubulk
del /S Dungeons\*.uexp
del /S Dungeons\*.umap
del /S Dungeons\*.ufont

"%editorPath%\UE4Editor-Cmd.exe" "%ddp%\UE4Project\Dungeons.uproject" -run=cook -targetplatform=WindowsNoEditor

robocopy /job:Tools\configs\copy_cooked_assets

robocopy /S Precooked Dungeons