import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Name of the file within the working dirctory that has to be accessed",
                },
                "content":{
                    "type": "string",
                    "description":"The content that needs to be written into the specified file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        #GuardRails / Scope
        working_dir_abs = os.path.abspath(working_directory)
        file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, file_path]) == working_dir_abs


        if not valid_target_file:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(working_dir_abs), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
