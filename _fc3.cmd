@echo off
cd /d C:\Users\trist\Development\BitConcepts\glossa-lab
python -c "import sys,os,asyncio; sys.path.insert(0,'backend'); os.environ['GLOSSA_DATA_DIR']='backend/data'; from glossa_lab.api.foundation_check import run_foundation_check; r=asyncio.run(run_foundation_check()); s=r['summary']; print('PASS=%d FAIL=%d WARN=%d -> %s'%(s['n_pass'],s['n_fail'],s['n_warn'],s['overall_status']))"
