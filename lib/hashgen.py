import subprocess
def get_hash(): print(subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip())
get_hash()