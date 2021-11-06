import os
from sys import platform

def get_path(filename:str):
    if platform == "darwin": 
        path = str(os.path.dirname(os.path.realpath(__file__)))+ f"/{filename}"
    elif platform == "win32":
        path = str(os.path.dirname(os.path.realpath(__file__)))+ f"\\{filename}"
    elif platform == "linux" or platform == "linux2":
        path = str(os.path.dirname(os.path.realpath(__file__)))+ f"/{filename}"

    return path 

#print(get_path("SD FOTOS")+"/")