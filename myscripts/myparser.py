def getsorption(file:str):

    with open(file,'r') as f:
        lines = f.readlines()
        
    data = {}
    for idx, line in enumerate(lines):
        if 'Average loading excess [cm^3 (STP)/cm^3 framework]' in line:
            break
        
    data['excess_cm_cm'] = float(lines[idx].split()[-4])
    data['excess_cm_gr'] = float(lines[idx-1].split()[-4])
    data['excess_mg_gr'] = float(lines[idx-2].split()[-4])
    data['excess_mo_kg'] = float(lines[idx-3].split()[-4])
    data['absolute_cm_cm'] = float(lines[idx-13].split()[-4])
    data['absolute_cm_gr'] = float(lines[idx-14].split()[-4])
    data['absolute_mg_gr'] = float(lines[idx-15].split()[-4])
    data['absolute_mo_kg'] = float(lines[idx-16].split()[-4])

    return data

def gethelium(file:str):
    with open(file,'r') as f:
        lines = f.readlines()
        

    for line in lines:
        if '[helium] Average Widom Rosenbluth-weight:' in line:
            heliumvoidfraction = float(line.split()[-4])
            break


    return heliumvoidfraction