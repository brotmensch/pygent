import os
import subprocess


def run_python_file(working_directory,file_path,args=[]):
    try:
        full_path =os.path.join(working_directory,file_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
            return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        elif not os.path.exists(os.path.abspath(full_path)):
            return(f'Error: File "{file_path}" not found.')
        elif not full_path.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file.')
        else:
            result=subprocess.run(
                ["python",
                 file_path]+list(args),
                 capture_output=True,
                 text=True,
                 timeout=30,
                 cwd=working_directory)
            stdout=result.stdout
            stderr=result.stderr
            if len(stdout)==0 and len(stderr)==0:
                return"No output produced."
            
            if result.returncode!=0:
                stderr=f"{stderr} \n Process exited with code{result.returncode}"
            

            

            return (f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}")
                   
                   




    except Exception as e:
        return f"Error: executing Python file: {e}"












    