import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "List the content of a file in the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Name of the file within the working dirctory that has to be accessed",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        #GuardRails / Scope
        working_dir_abs = os.path.abspath(working_directory)
        file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, file_path]) == working_dir_abs


        if not valid_target_file:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: "{file_path}" is not a file'

        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error:{e}"
