from pathlib import Path
from pymatgen.io.cif import CifWriter
from pymatgen.core.structure import Structure
import os


def cleanciffile(workdir):
    cwd = os.getcwd()
    
    ciffilename = Path(workdir).glob('*.cif').__next__().name
    cleanciffilename = 'structure.cif'
    os.chdir(workdir)
    inputstructure = Structure.from_file(ciffilename).get_primitive_structure()
    CifWriter(inputstructure).write_file(cleanciffilename)
    with open(cleanciffilename,'r') as f:
        lines = f.readlines()
    
    for idx, line in enumerate(lines):
        if line.startswith('_space_group_IT_number'):
            lines[idx] = '_symmetry_Int_Tables_number'+'      '+f'{line.split()[-1]}'
        if line.startswith('_space_group_name_H-M_alt'):
            lines[idx] = '_symmetry_space_group_name_H-M'+'      '+f'{line.split()[-1]}'
        if line.startswith('_space_group_name_Hall'):
            lines[idx] = '_symmetry_space_group_name_H-M'+'      '+f'{line.split()[-1]}'
    with open(cleanciffilename,'w+') as f:
        f.writelines(lines)
    os.chdir(cwd)