import json, sys, os
sys.path.append(os.path.dirname(sys.executable))
reverse = False
input_path = None
output_path = None
for arg in sys.argv[1:]:
    if arg == '-reverse':
        reverse = True
    else:
        if input_path == None:
            input_path = arg
        else:
            if output_path == None:
                output_path = arg
else:
    if reverse:
        from ConversionTools import ObjectGroupToJavaWorld
        if input_path == None or output_path == None:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            if input_path == None:
                input_path = filedialog.askopenfilename(initialdir='/', title='Select file', filetypes=[('JSON file', '.json')])
                if input_path == '':
                    print('Error: No input path.')
                    input('Press Enter to continue...')
                    sys.exit(1)
            if output_path == None:
                output_path = filedialog.askdirectory()
                if output_path == '':
                    print('Error: No output path.')
                    input('Press Enter to continue...')
                    sys.exit(1)
        ObjectGroupToJavaWorld(input_path, output_path).convert()
    else:
        from ConversionTools import JavaWorldToObjectGroup
        from pretty_compact_json import stringify
        if input_path == None or output_path == None:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            if input_path == None:
                input_path = filedialog.askdirectory()
                if input_path == '':
                    print('Error: No input path.')
                    input('Press Enter to continue...')
                    sys.exit(1)
            objectgroup = JavaWorldToObjectGroup(input_path).convert()
            if output_path == None:
                output_path = filedialog.asksaveasfilename(initialdir='/', title='Select file', filetypes=[('JSON file', '.json')])
                if output_path == '':
                    print('Error: No output path.')
                    input('Press Enter to continue...')
                    sys.exit(1)
                if not output_path.endswith('.json'):
                    output_path += '.json'
            with open(output_path, 'w') as outfile:
                outfile.write(stringify(objectgroup))
        else:
            objectgroup = JavaWorldToObjectGroup(input_path).convert()
            with open(output_path, 'w') as outfile:
                outfile.write(stringify(objectgroup))
# okay decompiling JavaWorldToObjectGroup.exe_extracted/app_JavaToObjectGroup_v2.pyc