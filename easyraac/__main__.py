import sys
import os
file_path = os.path.dirname(__file__)
sys.path.append(file_path)
try:
    from . import Visual
except:
    import Visual

def rpct_main():
    print('EasyRAAC version=1.0')
    Visual.visual_create_blast(file_path)
    Visual.visual_create_aaindex(file_path)
    Visual.visual_create_raac(file_path)