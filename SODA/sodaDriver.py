## developed by soraya remaili
import os
import sys
import glob
import subprocess

pythonVersion = sys.executable
folder = os.path.abspath('./SODA')

psmFiles = glob.glob(os.path.join(folder, '**', '*PSM*.py'), recursive=True)

## loading in the possible values
seasons = [0, 1]
models = [1, 2, 3]

## going through all model combinations
for filename in psmFiles:
    for season in seasons:
        for model in models:
            print(f"Running {filename} with season = {season} and model = {model}")
            subprocess.run([pythonVersion, filename, '--season', str(season), '--model', str(model)])
