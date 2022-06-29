# Imports
from rich.prompt import Prompt, Confirm
from rich.progress import Progress
import subprocess
import sys
import os

def git_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

__version__ = git_hash()

# Create poetry env

class Project:
    def __init__(
        self,
        name,
        path
    ) -> None:
        self.name = name
        self.path = path

def proc_cmd_syn(cmd: list[str]) -> str:
    """
    Process syntax to match console supported standard
    ```python
    proc_cmd_syn(["python3", "-c", "print(\"Hello\")"])
    ```
    """
    return " ".join(
        f'"{token}"' if " " in token and token[0] not in {"'", '"'} else token
        for token in cmd
    )

class System:
    root = '.'
    assets = "assets"

    def resources(c):
        return str( System.root + "/" + System.assets + "/" + c )
    
    def pyversion() -> str:
        return subprocess.check_output(
            proc_cmd_syn(["python3", "-c", "\"import sys; print('.'.join([str(s) for s in sys.version_info[:3]]))\""]),
            shell=True,
        ).decode().strip()

class EnvHandler:
    def __init__(
        self,
        p: Project
    ) -> None:
        self.project_name = p.name
        self.project_path = p.path
    
    def compose(self):
        # Create 

        # poetry new my-folder --name my-package
        pyv = System.pyversion()

env = EnvHandler(
    Project(
        "test",
        os.getcwd()
    )
)
env.compose()


class Console:
    def __init__(
        self
    ) -> None:
        pass

    def run(self,args):
        # Show TUI
        if '--no-ascii' not in args:
            print(open(System.resources("art"),"r").read())
            print(f"Version {__version__} on Python {System.pyversion()}")

console = Console()
console.run(
    sys.argv
)

import time

#with Progress() as progress:
#
#    task1 = progress.add_task("[red]Downloading...", total=1000)
#    task2 = progress.add_task("[green]Processing...", total=1000)
#    task3 = progress.add_task("[cyan]Cooking...", total=1000)
#
#    while not progress.finished:
#        progress.update(task1, advance=0.5)
#        progress.update(task2, advance=0.3)
#        progress.update(task3, advance=0.9)
#        time.sleep(0.02)
