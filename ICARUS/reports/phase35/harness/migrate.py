import sys
from pathlib import Path
sys.path.insert(0,'/workspace/work/munza69/ICARUS')
import verify_frontier_backup as m
m.ROOT=Path(__file__).resolve().parent/'tested/ICARUS_Cinematic_Refinement_Phase3_5_Lite'
raise SystemExit(m.main())
