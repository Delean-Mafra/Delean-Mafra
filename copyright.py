import os

def add_copyright_if_missing(folder_path):
    copyright_text = 'print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")'
    
    # Walk through all files in the directory and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Check if copyright text already exists
                if not any(copyright_text in line for line in lines):
                    # Find the first empty line after imports
                    new_lines = []
                    imports_done = False
                    copyright_added = False
                    
                    for line in lines:
                        if not copyright_added:
                            # Check if we're past the imports
                            if line.strip() and not line.strip().startswith(('import ', 'from ')):
                                imports_done = True
                            
                            # If we're past imports and find an empty line, add copyright
                            if imports_done and not line.strip():
                                new_lines.append(copyright_text + '\n')
                                new_lines.append('\n')  # Add an extra empty line for readability
                                copyright_added = True
                            
                        new_lines.append(line)
                    
                    # If we couldn't find a suitable empty line, add at the top after any existing imports
                    if not copyright_added:
                        final_lines = []
                        imports_done = False
                        copyright_added = False
                        
                        for line in lines:
                            if not copyright_added and not line.strip().startswith(('import ', 'from ')):
                                if not copyright_added:
                                    final_lines.append(copyright_text + '\n')
                                    final_lines.append('\n')
                                    copyright_added = True
                            final_lines.append(line)
                        
                        new_lines = final_lines

                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    
                    print(f'Added copyright notice to: {file}')
                else:
                    print(f'Copyright notice already exists in: {file}')

if __name__ == "__main__":
    folder_path = input("Digite o caminho da pasta para procurar arquivos Python: ")
    add_copyright_if_missing(folder_path)