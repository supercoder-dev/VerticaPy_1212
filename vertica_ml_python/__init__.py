# (c) Copyright [2018-2020] Micro Focus or one of its affiliates. 
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# |_     |~) _  _| _  /~\    _ |.
# |_)\/  |_)(_|(_||   \_/|_|(_|||
#    /                           
#              ____________       ______
#             /           `\     /     /
#            |   O         /    /     /
#            |______      /    /     /
#                   |____/    /     /
#          _____________     /     /
#          \           /    /     /
#           \         /    /     /
#            \_______/    /     /
#             ______     /     /
#             \    /    /     /
#              \  /    /     /
#               \/    /     /
#                    /     /
#                   /     /
#                   \    /
#                    \  /
#                     \/
#
#
# \  / _  __|_. _ _   |\/||   |~)_|_|_  _  _ 
#  \/ (/_|  | |(_(_|  |  ||_  |~\/| | |(_)| |
#                               /            
# Vertica-ML-Python allows user to create vDataFrames (Virtual Dataframes). 
# vDataFrames simplify data exploration, data cleaning and MACHINE LEARNING     
# in VERTICA. It is an object which keeps in it all the actions that the user 
# wants to achieve and execute them when they are needed.    										
#																					
# The purpose is to bring the logic to the data and not the opposite !
#
#               
__version__ = "1.0-beta"
__author__ = "Badr Ouali"
__author_email__ = "badr.ouali@microfocus.com"
__description__ = """Vertica-ML-Python simplifies data exploration, data cleaning and machine learning in Vertica."""
__url__ = "https://github.com/vertica/vertica_ml_python/"
__license__ = "Apache License, Version 2.0"

# vDataFrame
from vertica_ml_python.vdataframe import *

# Utilities
from vertica_ml_python.utilities import *

# Connect
from vertica_ml_python.connections.connect import *

# Learn
import vertica_ml_python.learn
