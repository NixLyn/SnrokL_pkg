# LOCAL
from File_Man import File_man
from de_confuse import DeFuse_
from port_figs import PortFig

# SYS_BASE
import subprocess
from threading import Thread
import time
import socket
import struct
import textwrap
import sys

# ! Break Down IP-v4-Packets
class ICMP_Packet():
    def __init__(self, **kw):
        super(ICMP_Packet, self).__init__(**kw)
        self.FM                 = File_man()
        self.DF                 = DeFuse_()
        self.PF                 = PortFig()



    def icmp_proto_(self, proto, data, checksum,  mode_):
        try:
            # ! ICMP Hex Segments
            hex_seg = self.DF.break_payload_hex_view(data)
            if "v" in str(mode_):
                print(f"[ICMP]:[DATA]:[{str(data)}]")
                

            
        except Exception as e:
            print(f"[E]:[ICMP_PROTO]:[{str(e)}]")
