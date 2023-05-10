import os
import shutil
from textwrap import dedent
from pymatgen.io.vasp import Incar, Poscar, Potcar, Kpoints
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifWriter
from statistics import mean

def addchargetocif(workdir):
    
    cwd = os.getcwd()
    os.mkdir('/'.join([workdir, 'charge']))
    os.chdir('/'.join([workdir, 'charge']))
    shutil.copy('../structure.cif','structure.cif')
    
    
    vaspparameters = {
        "ENCUT": 400,
        "GGA": "Pe",
        "IALGO": 48,
        "ICHARG": 2,
        "ISMEAR": 0,
        "ISTART": 0,
        "LAECHG": True,
        "LCHARG": True,
        "LREAL": "Auto",
        "NPAR": 4,
        "NSW": 0,
        "PREC": "Accurate",
        "SIGMA": 0.01,
        "SYSTEM": "DDEC",
    }
    Incar(vaspparameters).write_file("INCAR")
    crystalstructure = Structure.from_file('structure.cif')
    Poscar(crystalstructure).write_file("POSCAR")
    Potcar([E.name for E in crystalstructure.composition.elements]).write_file("POTCAR")
    Kpoints().write_file("KPOINTS")

    vasp_commmand =  dedent(''' 
                     export PATH=/opt/VASP/5.4.4-gzbuild/bin:$PATH
                     mpirun -np 56 vasp_std > vasp.out 2>vasp.err 
                     ''')
    os.system(vasp_commmand)
    
    with open("job_control.txt",'w+') as f:
        f.write(r'''<net charge>
    0.0
    </net charge>

    <periodicity along A, B, and C vectors>
    .true.
    .true.
    .true.
    </periodicity along A, B, and C vectors>

    <atomic densities directory complete path>
    /opt/chargemol/chargemol_09_26_2017/atomic_densities/
    </atomic densities directory complete path>

    <charge type>
    DDEC6
    </charge type>''')

    os.system('/opt/chargemol/chargemol_09_26_2017/chargemol_FORTRAN_09_26_2017/compiled_binaries/linux/Chargemol_09_26_2017_linux_parallel ')
    
    
    s = Structure.from_file('CONTCAR')
    CifWriter(s).write_file('temp.cif')

    with open('temp.cif','r') as f:
        lines = f.readlines()
    idx = lines.index(' _atom_site_occupancy\n')

    with open('DDEC6_even_tempered_net_atomic_charges.xyz','r') as f:
        lines2 = f.readlines()
        atommount = int(lines2[0].strip())
        l = []
        for line in lines2[2:2+atommount]:
            l.append(float(line.split()[-1]))
    m=mean(l)
    newl = [round(x-m,10) for x in l]


    for idx2,c in enumerate(newl):
        lines[idx+1+idx2] = lines[idx+1+idx2].replace('\n',f'    {c}\n')
        
        
    lines.insert(idx+1,' _atom_site_charge\n')

    with open('structure_charged.cif','w') as f:
        f.writelines(lines)   
        
    os.chdir(cwd)
