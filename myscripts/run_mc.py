import os
from pathlib import Path
import shutil
from textwrap import dedent
from math import ceil
from pymatgen.core.structure import Structure
from myscripts.myparser import gethelium,getsorption


def runhelium(workdir:str):
    
    cwd = os.getcwd()
    os.mkdir(workdir+'/helium')
    os.chdir(workdir+'/helium')
    
    shutil.copy(f'../charge/structure_charged.cif','structure_charged.cif')
    shutil.copy('/opt/RASPA/share/raspa/molecules/TraPPE/helium.def','helium.def')
    shutil.copy('/opt/RASPA/share/raspa/forcefield/DDEC_UFF_RESP_UFF/force_field_mixing_rules.def','force_field_mixing_rules.def')
    shutil.copy('/opt/RASPA/share/raspa/forcefield/DDEC_UFF_RESP_UFF/pseudo_atoms.def','pseudo_atoms.def')

    structure = Structure.from_file('structure_charged.cif')
    input_script = dedent("""
                        SimulationType                MonteCarlo
                        NumberOfCycles                500
                        PrintEvery                    50
                        PrintPropertiesEvery          50
                        
                        Forcefield                    Local
                        CutOff                        14.0

                        Framework                     0
                        FrameworkName                 structure_charged
                        UnitCells                     {a} {b} {c}
                        ExternalTemperature           298.0

                        Component 0 MoleculeName             helium
                                    MoleculeDefinition       Local
                                    WidomProbability         1.0
                                    CreateNumberOfMolecules  0
                        """.format(a=ceil(14.0/structure.lattice.a),b=ceil(14.0/structure.lattice.b),c=ceil(14.0/structure.lattice.c))).strip()
    with open('simulation.input','w+') as f:
        f.write(input_script)
        
    command = dedent(''' 
                     export RASPA_DIR=/opt/RASPA
                     $RASPA_DIR/bin/simulate simulation.input 1>raspa.out 2>raspa.err 
                     ''')
    os.system(command)

    datafile = Path('Output/System_0').glob('*.data').__next__().name
    result = gethelium('/'.join(['Output','System_0',datafile]))
    
    os.chdir(cwd)
    return result
    
def runmc(workdir,adsorbate,heliumvoidfraction):
    
    cwd = os.getcwd()
    os.mkdir('/'.join([workdir,adsorbate]))
    os.chdir('/'.join([workdir,adsorbate]))
    
    shutil.copy(f'../charge/structure_charged.cif','structure_charged.cif')
    shutil.copy(f'/opt/RASPA/share/raspa/molecules/FULLUFF/{adsorbate}.def',f'{adsorbate}.def')
    shutil.copy('/opt/RASPA/share/raspa/forcefield/DDEC_UFF_RESP_UFF/force_field_mixing_rules.def','force_field_mixing_rules.def')
    shutil.copy('/opt/RASPA/share/raspa/forcefield/DDEC_UFF_RESP_UFF/pseudo_atoms.def','pseudo_atoms.def')
    structure = Structure.from_file('structure_charged.cif')
    input_script = dedent("""
                        SimulationType                              MonteCarlo
                        NumberOfCycles                              100
                        NumberOfInitializationCycles                100
                        PrintEvery                                  20

                        RestartFile                                 no

                        Movies                                      yes
                        WriteMoviesEvery                            200

                        ComputeDensityProfile3DVTKGrid              yes
                        WriteDensityProfile3DVTKGridEvery           200
                        DensityProfile3DVTKGridPoints               200 200 200
                        AverageDensityOverUnitCellsVTK              yes
                        DensityAverageingTypeVTK                    FullBox

                        Forcefield                                  Local
                        UseChargesFromCIFFile                       yes
                        CutOffVDW                                   14.0
                        ChargeMethod                                Ewald
                        EwaldPrecision                              1e-6

                        Framework                                   0
                        FrameworkName                               structure_charged
                        UnitCells                                   {a} {b} {c}
                        HeliumVoidFraction                          {heliumvoidfraction}
                        ExternalPressure                            101325.0
                        ExternalTemperature                         298K.0

                        Component 0 MoleculeName                    {molname}
                                    MoleculeDefinition              Local
                                    FugacityCoefficient             1.0
                                    TranslationProbability          1.0
                                    RotationProbability             1.0
                                    ReinsertionProbability          1.0
                                    CBMCProbability                 1.0
                                    SwapProbability                 1.0
                                    CreateNumberOfMolecules         0
                        """.format(a=ceil(14.0/structure.lattice.a),b=ceil(14.0/structure.lattice.b),c=ceil(14.0/structure.lattice.c),heliumvoidfraction=heliumvoidfraction,molname=adsorbate)).strip()



    with open('simulation.input','w+') as f:
        f.write(input_script)
        
    command = dedent(''' 
                     export RASPA_DIR=/opt/RASPA
                     $RASPA_DIR/bin/simulate simulation.input 1>raspa.out 2>raspa.err 
                     ''')
    os.system(command)

    datafile = Path('Output/System_0').glob('*.data').__next__().name
    result = getsorption('/'.join(['Output','System_0',datafile]))
    
    os.chdir(cwd)
    return result