SET /p packageOutput= < Tools\settings\package_output.txt

python Tools\u4pak.py pack "%packageOutput%" Dungeons -p