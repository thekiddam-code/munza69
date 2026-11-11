import sys
from pathlib import Path
sys.path.insert(0,'/workspace/work/munza69/ICARUS')
import verify_frontier_backup as m
m.ROOT=Path(__file__).resolve().parent/'tested/ICARUS_SOL_Command_Interface_Phase4_Lite'
raise SystemExit(m.main())
