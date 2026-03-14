from pycomm3 import LogixDriver
from rich import print
import sys

#Set PLC IP Address here
PLC_IP = '10.22.128.92'

def flatten_tags(tags):
    def flatten_struct(struct):
        for attr in struct['attributes']:
            yield attr
            if struct['internal_tags'][attr]['tag_type'] == 'struct':
                yield from (f'{attr}.{x}' for x in flatten_struct(struct['internal_tags'][attr]['data_type']))
                
    
    for tag, _def in tags.items():
        yield tag
        if _def['tag_type'] == 'struct':
            yield from (f'{tag}.{attr}' for attr in flatten_struct(_def['data_type']))
        
    
    
try:
    with LogixDriver(PLC_IP) as plc:
        print(plc.tags)  # same as get_tag_list, set automatically when connection is opened
        print(list(flatten_tags(plc.tags)))

except Exception as e:
    print(f"Error occurred: {e}", file=sys.stderr)