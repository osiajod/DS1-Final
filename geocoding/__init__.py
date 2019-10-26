
google_keys = []
osm_keys = []


with open('./google_keys') as fp:
    temp = fp.readlines()
    for i in temp:
        google_keys.append(i.strip())

with open('./osm_keys') as fp2:
    temp = fp2.readlines()
    for i in temp:
        osm_keys.append(i.strip())