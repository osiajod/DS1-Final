import os
from pathlib import Path
google_keys = []
osm_keys = []

p = str(Path(__file__).resolve().parent)

with open(p+'/google_keys') as fp:
    temp = fp.readlines()
    for i in temp:
        google_keys.append(i.strip())

with open(p+'/osm_keys') as fp2:
    temp = fp2.readlines()
    for i in temp:
        osm_keys.append(i.strip())

