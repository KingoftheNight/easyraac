# import package
import os
import subprocess
now_path = os.getcwd()
blast_path = os.path.dirname(__file__)
import sys
sys.path.append(blast_path)
from Visual import visual_longcommand

# original psiblast
def blast_psiblast(file, database, number, ev, out=now_path):
    save_path = os.path.join(out, file.split('.')[0] + '.pssm')
    database_path = os.path.join(os.path.join(blast_path, 'blastDB'), database)
    command = visual_longcommand(file, database_path, number, ev, save_path)
    outcode = subprocess.Popen(command, shell=True)
    if outcode.wait() != 0:
        print('\r\tProblems', end='', flush=True)
    if 'A' in os.listdir(out):
        os.remove(os.path.join(out, 'A'))
    if 'A' in os.listdir(now_path):
        os.remove(os.path.join(now_path, 'A'))
