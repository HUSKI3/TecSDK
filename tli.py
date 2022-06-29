# Imports

# --- Rich ---
from rich import print
from rich.prompt import Prompt
from rich.progress import Progress, wrap_file
from rich.console import Console as RConsole
from rich.markdown import Markdown
from rich.text import Text
# ------------
rconsole = RConsole()

# --- Args ---
import argparse
# ------------

# --- Path ---
from pathlib import Path
# ------------
from urllib.request import urlopen
from urllib import error as URLError
import json
import subprocess
import sys
import os

def git_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

__version__ = git_hash()

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
    
    def python() -> str:
        '''
        Get Python binary path
        '''
        return sys.executable

    def pyversion() -> str:
        return subprocess.check_output(
            proc_cmd_syn(["python3", "-c", "\"import sys; print('.'.join([str(s) for s in sys.version_info[:3]]))\""]),
            shell=True,
        ).decode().strip()

    def run_py(line) -> str:
        return subprocess.check_output(
            proc_cmd_syn([System.python(), "-c", '"'+line+'"' ]),
            shell=True,
        ).decode().strip()
    
    def run_cmd(line = None) -> str:
        if not line:
            raise Exception("System - No valid line supplied")
        return subprocess.check_output(
            proc_cmd_syn(line.split(' ')),
            shell=True,
        ).decode().strip()

    def create_dir(
        root: str,
        target: str
    ) -> str:
        '''
        Create a directory and return the path to the new directory
        '''
        path = os.path.join(root, target)
        os.mkdir(path)
        return path+'poop'

    def create_file(
        name,
        path,
        contents = ""
    ):
        with open(path + '/' + name, "w+") as f:
            f.write(contents)

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




class Console:
    def __init__(
        self
    ) -> None:
        pass

    def new_project_menu(self):
        # Create new project
        env = EnvHandler(
            Project(
                "test",
                os.getcwd()
            )
        )
        env.compose()
        pass

    def help_menu(self):
        pass

    def install(
        self,
        args
    ):
        pass


    def run(
            self,
            args: list[str]
        ):

        # Show TUI
        if not args.no_ascii:
            print(open(System.resources("art"),"r").read())
            print(f"Version {__version__} on Python {System.pyversion()}")

        if args.debug:
            print(args, "Debug Mode :warning:")

        # Choices
        if not args.parse:
            opts = {
                "new": self.new_project_menu,
                "help": self.help_menu,
                "exit": exit,
            }
            md = Markdown(open(System.resources("menu"),'r').read())
            rconsole.print(md)
            while 1:
                _ = Prompt.ask(">", choices=["new", "help", "exit"], default="")
                if _ in opts:
                    opts[_]()


console = Console()

# Parse args
parse = argparse.ArgumentParser()

parse.add_argument('--no-ascii',
                       action='store_true',
                       help='enable the tui format')
parse.add_argument('--parse',
                       action='store_true',
                       help='parse from a command')
parse.add_argument('--debug',
                       action='store_true',
                       help='enable debugging')
parse.add_argument('--install-full',
                       action='store_true',
                       help='install full tecsdk locally')

args = parse.parse_args()

if not args.install_full:
    console.run(
        args
    )
else:
    # Prepare for the install
    home = str(Path.home())
    target = '.tecsdk'
    
    if not os.path.exists(os.path.join(home, target)):
        target = System.create_dir(home, target)
        print("Created directory ✅")
    else: print("Exists ✅"); target = os.path.join(home, target)

    os.chdir(target)

    response = urlopen("http://20.56.72.151:8000/tecsdk.recipe")
    size = int(response.headers["Content-Length"])
    recipe = []

    with wrap_file(response, size, description="[red]Downloading recipe ...") as file:
        for line in file:
            recipe.append(line.decode("utf-8"))

    #if args.debug:
    #    print(recipe)

    # Parse recipe
    recipe = json.loads(' '.join(recipe))
    
    text = Text(f"Preparing recipe [{recipe['project']}]:")
    text.stylize("bold blue")
    rconsole.print(text)

    for component in recipe['components']:
        data = []
        try:
            response = urlopen(component['download'])
            size = int(response.headers["Content-Length"])
            with wrap_file(response, size, description=f"[red]\[{component['name']}]") as file:
                for line in file:
                    data.append(line)
        except URLError.HTTPError:
            print(f"Failed to download resource \[{component['name']}] at {component['download']}")

        if data:
            file_name = component['download'].rsplit('/',1)[1]
            with open(file_name, 'wb+') as f:
                f.writelines(data)
