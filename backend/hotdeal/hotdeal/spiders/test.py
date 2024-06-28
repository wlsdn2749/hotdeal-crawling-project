import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import DataUtils

# print(os.path.normpath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
print(DataUtils.get_current_development())
# from dotenv import load_dotenv
# load_dotenv()
# development = 

# print( os.environ.get("development") )