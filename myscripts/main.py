from myscripts.run_cif import cleanciffile
from myscripts.run_charge import addchargetocif
from myscripts.run_mc import runmc, runhelium
from myscripts.sendemail import sendresult
from textwrap import dedent

def run(workdir,adsorbate,mailaddress):
    cleanciffile(workdir)
    addchargetocif(workdir)
    heliumvoidfraction=runhelium(workdir)
    result=runmc(workdir,adsorbate,heliumvoidfraction)
    
    sendresult(str(result),mailaddress)
    

if __name__ =="__main__":
    
    run('/home/guoxiang/Documents/practice/django-web/websorption/uploaddata/fsdf/23-05-09-19-49-15','ethane','zhaoguoxiang@fjirsm.ac.cn')