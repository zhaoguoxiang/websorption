import os
import shutil
from pathlib import Path


    
    
def get_res_data(res_file):
    res_dict = {}
    with open(res_file, "r") as f:
        data = f.readlines()[0].split()
        res_dict["GCD"] = float(data[1])
        res_dict["PLD"] = float(data[2])
        res_dict["LCD"] = float(data[3])
        res_dict["PLD_a"] = float(data[4])
        res_dict["PLD_b"] = float(data[5])
        res_dict["PLD_c"] = float(data[6])
        res_dict["LCD_a"] = float(data[7])
        res_dict["LCD_b"] = float(data[8])
        res_dict["LCD_c"] = float(data[9])

    return res_dict


def get_sa_data(sa_file):
    sa_dict = {}
    with open(sa_file, "r") as f:
        lines = f.readlines()
        data = lines[0].split()
        sa_dict["Unitcell_volume"] = float(data[3])
        sa_dict["Density"] = float(data[5])
        sa_dict["ASA_A^2"] = float(data[7])
        sa_dict["ASA_m^2/cm^3"] = float(data[9])
        sa_dict["ASA_m^2/g"] = float(data[11])
        sa_dict["NASA_A^2"] = float(data[13])
        sa_dict["NASA_m^2/cm^3"] = float(data[15])
        sa_dict["NASA_m^2/g"] = float(data[17])

        #
        line_1 = lines[1].split()
        Nc = int(line_1[1])
        l = [0.0] * 10
        if Nc == 0:
            sa_dict["Channel_surface_area_A^2"] = l
        elif Nc<=10:
            l[0:Nc] = [float(x) for x in line_1[3:]]
            sa_dict["Channel_surface_area_A^2"] = l
        elif Nc>10:
            l[0:10] = [float(x) for x in line_1[3:13]]
            sa_dict["Channel_surface_area_A^2"] = l
            
        line_2 = lines[2].split()
        Np = int(line_2[1])
        l = [0.0] * 10
        if Np == 0:
            sa_dict["Pocket_surface_area_A^2"] = l
        elif Np<=10:
            l[0:Np] = [float(x) for x in line_2[3:]]
            sa_dict["Pocket_surface_area_A^2"] = l
        elif Np > 10:
            l[0:10] = [float(x) for x in line_2[3:13]]
            sa_dict["Pocket_surface_area_A^2"] = l
    return sa_dict


def get_vol_data(vol_file):
    vol_dict = {}
    with open(vol_file, "r") as f:
        lines = f.readlines()
        data = lines[0].split()

        vol_dict["AV_A^3"] = float(data[7])
        vol_dict["AV_Volume_fraction"] = float(data[9])
        vol_dict["AV_cm^3/g"] = float(data[11])
        vol_dict["NAV_A^3"] = float(data[13])
        vol_dict["NAV_Volume_fraction"] = float(data[15])
        vol_dict["NAV_cm^3/g"] = float(data[17])

        line_1 = lines[1].split()
        Nc = int(line_1[1])
        l = [0.0] * 10
        if Nc == 0:
            vol_dict["Channel_volume_A^3"] = l
        elif Nc<=10:
            l[0:Nc] = [float(x) for x in line_1[3:]]
            vol_dict["Channel_volume_A^3"] = l
        elif Nc>10:
            l[0:10] = [float(x) for x in line_1[3:13]]
            vol_dict["Channel_volume_A^3"] = l
        line_2 = lines[2].split()
        Np = int(line_2[1])
        l = [0.0] * 10
        if Np == 0:
            vol_dict["Pocket_volume_A^3"] = l
        elif Np<=10:
            l[0:Np] = [float(x) for x in line_2[3:]]
            vol_dict["Pocket_volume_A^3"] = l
        elif Np>10:
            l[0:10] = [float(x) for x in line_2[3:13]]
            vol_dict["Pocket_volume_A^3"] = l
    return vol_dict


def get_volpo_data(volpo_file):
    volpo_dict = {}
    with open(volpo_file, "r") as f:
        lines = f.readlines()
        data = lines[0].split()
        volpo_dict["POAV_A^3"] = float(data[7])
        volpo_dict["POAV_Volume_fraction"] = float(data[9])
        volpo_dict["POAV_cm^3/g"] = float(data[11])
        volpo_dict["PONAV_A^3"] = float(data[13])
        volpo_dict["PONAV_Volume_fraction"] = float(data[15])
        volpo_dict["PONAV_cm^3/g"] = float(data[17])

        volpo_dict["probe_ctr_A_fract"] = float(lines[2].split()[5])
        volpo_dict["probe_ctr_NA_fract"] = float(lines[2].split()[6])
        volpo_dict["A_fract"] = float(lines[2].split()[7])
        volpo_dict["NA_fract"] = float(lines[2].split()[8])
        volpo_dict["narrow_fract"] = float(lines[2].split()[9])
        volpo_dict["ovlp_fract"] = float(lines[2].split()[10])

    return volpo_dict


def batch_data(work_dir):
    data_dict = {}
    current_path = os.getcwd()
    for itemdir in Path(work_dir).iterdir():
        os.chdir(itemdir)
        res_file = list(itemdir.glob("*.res"))[0]
        res = get_res_data(res_file.name)
        sa_file = list(itemdir.glob("*.sa"))[0]
        sa = get_sa_data(sa_file.name)
        vol_file = list(itemdir.glob("*.vol"))[0]
        vol = get_vol_data(vol_file.name)
        volpo_file = list(itemdir.glob("*.volpo"))[0]
        volpo = get_volpo_data(volpo_file.name)
        data_dict[itemdir.stem] = {**res, **sa, **vol, **volpo}
        os.chdir(current_path)
    return data_dict


def get_data(workdir):
    res = get_res_data('/'.join([workdir,'zeoppfeatures','structure.res']))
    sa = get_sa_data('/'.join([workdir,'zeoppfeatures','structure.sa']))
    vol = get_vol_data('/'.join([workdir,'zeoppfeatures','structure.vol']))
    volpo = get_volpo_data('/'.join([workdir,'zeoppfeatures','structure.volpo']))
    
    return  {**res, **sa, **vol, **volpo}


def runzeo(workdir):
    
    cwd = os.getcwd()
    os.mkdir('/'.join([workdir,'zeoppfeatures']))
    os.chdir('/'.join([workdir,'zeoppfeatures']))
    
    shutil.copy(f'../structure.cif','structure.cif')
    
    os.system('srun /opt/zeopp/zeo++-0.3/network -ha -resex                   structure.res   structure.cif > /dev/null ')
    os.system('srun /opt/zeopp/zeo++-0.3/network -ha -sa 1.86 1.86 10000                   structure.sa   structure.cif > /dev/null ')
    os.system('srun /opt/zeopp/zeo++-0.3/network -ha -vol 0.0 0.0 100000                   structure.vol   structure.cif > /dev/null ')
    os.system('srun /opt/zeopp/zeo++-0.3/network -ha -volpo 1.86 1.86 100000                   structure.volpo  structure.cif > /dev/null ')
    
    os.chdir(cwd)
    
    
