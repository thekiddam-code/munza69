import sys
from pathlib import Path
sys.path.insert(0,'/workspace/work/munza69/ICARUS')
import verify_frontier_backup as m
m.ROOT=Path(__file__).resolve().parent/'tested/ICARUS_Phase4_1_Command_Bridge_Lite'
raise SystemExit(m.main())
