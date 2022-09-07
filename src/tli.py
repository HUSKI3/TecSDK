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
from subprocess import Popen, PIPE

# Update git_hash to instead check the .hash file created during each build
def git_hash() -> str:
    if os.path.exists(".hash"):
        return open(".hash","r").read().strip() # cyclotron 5000
    else: return "0.0.0-dev"

# Assume OpenJDK is installed
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

__version__ = git_hash()
home = str(Path.home())
target = '.tecsdk'

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
    config_file = json.load(open("config", "r"))

    def config(e):
        if e in System.config_file:
            return System.config_file[e]

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
        return path
    
    def remove_file(
        root: str,
        target: str
    ) -> str:
        if os.path.exists(os.path.join(home, target)):
            os.remove(os.path.join(root, target))

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

        # Run python version checks first 
        if System.pyversion() in System.config("supported_python"):
            compatible = "✅"
        else: compatible = "❌ Unsupported"

        # Show TUI
        if not args.no_ascii:
            print(open(System.resources("art"),"r").read())
            print(f"Version {__version__} on Python {System.pyversion()} {compatible}")


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
                try:
                    _ = Prompt.ask(">", choices=["new", "help", "exit"], default="")
                    if _ in opts:
                        opts[_]()
                except EOFError:
                    raise Exception("Sorry, running the tui is not yet supported in Docker. Please use --parse {...} instead")
        
        else:
            args.parse = """
            {
                "name": "test",
                "path": "./newfolder/",
                "author": "HUSKI3"
            }"""

            # Parse 
            project_data = json.loads(args.parse)
            if {
                "name",
                "path",
                "author"
            } <= project_data.keys():
                pass
            else:
                print("Not yet implemented")


console = Console()
from time import sleep

global CoreService
CoreService = None

def startCore():
    os.chdir(
        os.path.join(os.path.join(home, target), "bundle")
    )
    CoreService = Popen(["python3", "main.py"], stdin=PIPE, stdout=PIPE)
    #time.sleep(5)
    #l = CoreService.stdout.readlines()
    print(f"Service started with pid: {CoreService.pid}")
    # Cycle so docker doesnt kill us
    while True: sleep(1)

def statusCore():
    os.chdir(
        os.path.join(home, target)
    )
    os.system("tree")
    l = CoreService.stdout.readlines()
    print(l)


actions = {
    "start": startCore,
    #"stop": stopCore,
    "status": statusCore
}

# Parse args
parse = argparse.ArgumentParser()

parse.add_argument('mode', choices=['start', 'stop', 'status'], nargs="?")

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
parse.add_argument('--check-recipe',
                       action='store_true',
                       help='Check recipe from the dist server')

args = parse.parse_args()

if not args.install_full\
    and not args.check_recipe\
        and not args.mode:
    console.run(
        args
    )
elif args.mode:
    actions[args.mode]()
else:
    # Prepare for the install
    if not args.no_ascii:
        print(open(System.resources("art"),"r").read())
        print("Preparing bundle and resources...")

    # Clean previously downloaded files
    if not args.check_recipe:
        for file in [
            "demo.tar.xz",
            "tcore-bundle.tar.gz"
        ]:
            System.remove_file(home, target+'/'+file)

        if System.pyversion() not in System.config("supported_python"):
            print(f"❌ Unsupported Python version ({System.pyversion()}) - Aborting installation")
            quit()

        if not os.path.exists(os.path.join(home, target)):
            target = System.create_dir(home, target)
            print("Created directory ✅")
        else: print("Exists ✅"); target = os.path.join(home, target)

        os.chdir(target)

    response = urlopen(System.config("recipe_url"))
    size = int(response.headers["Content-Length"])
    recipe = []

    with wrap_file(response, size, description="[red]Downloading recipe ...") as file:
        for line in file:
            recipe.append(line.decode("utf-8"))

    if args.check_recipe:
        print(recipe)
        quit()
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

        # TODO: Change this, add proper unpackaging
        if ".tar.gz" in file_name:
            os.system(f"tar xf {file_name}")
