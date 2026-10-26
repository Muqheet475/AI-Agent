import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a python file in the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Name of the file within the working dirctory that has to be accessed",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description":"An optional parameter that defaults to None if no CLI arguments are provided otherwise executes the python file with the argument",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        #GuardRails / Scope
        file=file_path
        working_dir_abs = os.path.abspath(working_directory)
        file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, file_path]) == working_dir_abs


        if not valid_target_file:
            return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path):
            return f'Error: "{file}" does not exist'
        if not file.endswith('py'):
            return f'Error: "{file}" is not a Python file'

        command = ["python", file_path]
        if args:
            command.extend(args)
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
