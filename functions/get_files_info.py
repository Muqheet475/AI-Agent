import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        #GuardRails / Scope
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs


        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        try:
            dir_content = os.listdir(target_dir)
            file_data=[]
            for i in dir_content:
                file_data.append((f'-{i}: file_size={os.path.getsize(f'{target_dir}/{i}')}, is_dir={os.path.isdir(f'{target_dir}/{i}')}'))

            file_details='\n'.join(file_data)
            return file_details
        except:
            raise Exception("Failed to get directory content")



    except Exception as e:
        return f"Error: {e}"
