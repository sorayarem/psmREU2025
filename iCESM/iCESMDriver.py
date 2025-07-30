## developed by soraya remaili
import os
import sys
import glob
import subprocess

pythonVersion = sys.executable
folder = os.path.abspath('./iCESM')

psmFiles = glob.glob(os.path.join(folder, '**', '*PSM*.py'), recursive=True)

## loading in the possible values
seasons = [0, 1]
models = [1, 2, 3]
isotopes = [0, 1]

## going through all model combinations
for filename in psmFiles:
    for isotope in isotopes:
        for season in seasons:
            for model in models:
                print(f"Running {filename} with season = {season} and model = {model} and isotope = {isotope}")
                subprocess.run([pythonVersion, filename, '--season', str(season), '--model', str(model), '--iso', str(isotope)])
