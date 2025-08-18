import os
from google.genai import types
def get_files_info(working_directory, directory="."):
    directory=os.path.join(working_directory,directory)
    if  not os.path.abspath(directory).startswith(os.path.abspath(working_directory)):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.isdir(os.path.abspath(directory)):
        return f'Error: "{directory}" is not a directory'

    
    else:
        content_list= os.listdir(directory)
        
        result="\n".join(
        get_content_string(item, directory) for item in content_list)
        return result if content_list else f'No files found in "{directory}"'   
            
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    
    
    
    

def get_content_string(item, directory):
        return f"- {item}: file_size= {os.path.getsize(directory + '/' + item)} bytes, is_dir={os.path.isdir(directory + '/' + item)}"