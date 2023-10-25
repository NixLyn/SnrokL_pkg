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
class IP_v_4():
    def __init__(self, **kw):
        super(IP_v_4, self).__init__(**kw)
        self.FM                 = File_man()
        self.DF                 = DeFuse_()
        self.PF                 = PortFig()



    def get_proto_(self, ):
        try:
            # ! IPv4_PACKET_SIZE -> 8
            if eth_proto == 8:
                version, header_length, ttl, proto, src, target, data_0 = self.PF.ipv4_packet(data)
                header_data = f"@[HEADER_DATA]::\n\t%[IPv4]:\
                    \n\t&[VERSION]:[{str(version)}]\
                    \n\t&[HEADER_LEN]:[{str(header_length)}]\
                    \n\t&[TTL]:[{str(ttl)}]\
                    \n\t&[PROTO]:[{str(proto)}]\
                    \n\t&[SRC]:[{str(src)}]\
                    \n\t&[TARGET]:[{str(target)}]\n"
                base_data = f"[BASE_DATA]::\
                    \n\t&[DEST]:[{str(dest_mac)}]\
                    \n\t&[SRC]:[{str(src_mac)}]\
                    \n\t&[ETH_PROTO]:[{str(eth_proto)}]\
                    \n\t\t&[DATA_RAW]:[{str(data_0)}]\n\n"
                if "v" in mode_:
                    print(f"[IPv4-/]:[SRC]:[{src}]&&[DST]:[{target}]\n")
                    print(base_data)
                    print(header_data)
                ts_data = f"[CP-#]:[{str(grab_count)}]\n"+header_data+base_data
                if "s" in mode_:
                    if src_ip in src:
                        self.FM.write_file("DATA/"+src_ip+"_v4_src.txt", ts_data, ";", "a+")
                        if "b" in mode_:
                            if "v" in mode_:
                                print("\n\n--BeastMode--\n\t-- [DATA-HASHI]:: \n")
                            self.DF.from_x_hex(data, grab_count, src_ip, mode_)
                    if target in dst_ip:
                        self.FM.write_file("DATA/"+dst_ip+"_v4_dst.txt", ts_data, ";", "a+")
                        if "b" in mode_:
                            if "v" in mode_:
                                print("\n\n--BeastMode--\n\t-- [DATA-HASHI]:: \n")
                            self.DF.from_x_hex(data, grab_count, dst_ip, mode_)

                # ! ICMP
                if proto == 1 and "ICMP" in typ:
                    icmp_type, code, checksum, data_1 = self.PF.icmp_packet(data)
                    icmp_set = f"[CP-#]:[{str(grab_count)}]\n"+f"\t@@[ICMP]:[{icmp_type}]\
                        \n\t\t[CODE]:[{code}]\
                        \n\t\t[CHECK_SUM]:[{checksum}]\
                        \n\t\t\t[{target}]:[DATA_RAW]:[{str(data_1)}]"
                    if "v" in mode_:
                        print("\t - [ICMP]:")
                        print(icmp_set)
                    if "s" in mode_:
                        if src_ip in src or src_ip in src_mac:
                            self.FM.write_file("DATA/"+dst_ip+"_icmp_src.txt", ts_data, ";", "a+")
                            if "b" in mode_:
                                if "s" in mode_:
                                    print("\n\n\t-- [DATA-HASHI]:: \n")
                                self.DF.from_x_hex(data, grab_count, src_ip, mode_)
                        if target in dst_ip or dst_ip in dest_mac:
                            self.FM.write_file("DATA/"+dst_ip+"_icmp_dst.txt", ts_data, ";", "a+")
                            if "b" in mode_:
                                if "s" in mode_:
                                    print("\n\n\t-- [DATA-HASHI]:: \n")
                                self.DF.from_x_hex(data, grab_count, dst_ip, mode_)
                # ! TCP
                if proto == 6 and "TCP" in typ:
                    src_port, dest_port, seq, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data = self.PF.tcp_segment(data)
                    base_in = f"[TCP]:\n\t[SRC_PORT]:[{str(src_port)}] :: [DEST_PORT]:[{str(dest_port)}]\n\t[SEQUENCE]:[{str(seq)}] :: [ACK_]:[{str(ack)}]"
                    flags_st = f"\t[FLAGS]:\t\t[URG]:[{str(flag_urg)}]\n\t\t[ACK]:[{str(flag_ack)}]\n\t\t[PSH]:[{str(flag_psh)}]\n\t\t[RST]:[{str(flag_rst)}]\n\t\t[SYN]:[{str(flag_syn)}]\n\t\t[FIN]:[{str(flag_fin)}]"
                    if "v" in mode_:
                        print("[TCP]:")
                        print(base_in)
                        print(flags_st)
                    wdata = f"[CP-#]:[{str(grab_count)}]\n"+f"[HEAD]:({base_in})\n[FLAGS]:({flags_st})"
                    if "s" in mode_:
                        if target in dst_ip:
                            self.FM.write_file("DATA/"+dst_ip+"_dest.txt", wdata, ";", "a+")
                        if src_ip in src:
                            self.FM.write_file("DATA/"+src_ip+"_src.txt", wdata, ";", "a+")
                    if "b" in mode_:
                        if "s" in mode_:
                            print("\n\n\t-- [DATA-HASHI]:: \n")
                        self.DF.from_x_hex(data, grab_count, file_name, mode_)
                
                # ! UDP
                if proto == 17 and "UDP" in typ:
                    src_port, dest_port, length, data = self.PF.udp_segment(data)
                    udp_head = f"[CP-#]:[{str(grab_count)}]\n"+f"\t[SRC_PORT]:[{src_port}]\n\t[DEST_PORT]:[{dest_port}]\n\t[LEN][{length}]"
                    if "v" in mode_:
                        print("[UDP]:")
                        print(f"\t\t[{target}]:[DATA]:[{data}]")
                        print(udp_head)
                    if "s" in mode_:
                        if dst_ip in dest_mac or dst_ip in target:
                            self.FM.write_file("DATA/"+dst_ip+"_udp_dst.txt", udp_head, ";", "a+")
                            if "b" in mode_:
                                if "v" in mode_:
                                    print("\n\n\t-- [DATA-HASHI]:: \n")
                                self.DF.from_x_hex(data, grab_count, dst_ip, mode_)
                        if src_ip in src_mac or src_ip in src:
                            self.FM.write_file("DATA/"+src_ip+"_udp_src.txt", udp_head, ";", "a+")
                            if "b" in mode_:
                                if "v" in mode_:
                                    print("\n\n\t-- [DATA-HASHI]:: \n")
                                self.DF.from_x_hex(data, grab_count, src_ip, mode_)
                # ! OTHER
                else:
                    data_ = self.PF.format_multi_line("\t\t", data)
                    if "v" in mode_:
                        print(f"[{target}]:[OTHER]:[DATA]:[{data_}]")
            # ! OTHER - OTHER
            else:
                data_ = self.PF.format_multi_line("\t\t", data)
                if "v" in mode_:
                    print(f"[{target}]:[DATA]:[{data_}]")
                if "b" in mode_:
                    self.DF.from_x_hex(data, grab_count, src_ip, mode_)
        except Exception as e:
            print(f"[E]:[GET_PROTO]:[{str(e)}]")
