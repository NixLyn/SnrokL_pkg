# SRC IMPORTS
from File_Man import File_man
from listen_1 import Listen_

# BASE IMPORTS
import asyncio
import websockets
import subprocess


# OOP
class SnrokL_Node():
    def __init__(self, **kw):
        super(SnrokL_Node, self).__init__(**kw)
        # SRCS
        self.FM         = File_man()
        self.Li         = Listen_()


        # ThisClass
        self.addr       = "127.0.0.1"
        self.port       = 8081
        self.server     = None
        self.clients    = []

    async def send_msg(self, client, msg_: str):
        """
        Return MSG to client
        """
        print(f"\n-[SENDING]:[{msg_}]\n-[TO]:[{client}]")
        await client.send(msg_)



    def get_cmd(self, msg_):
        try:
            new_rule        = ""
            stack_folder    = ""
            stols_ = msg_.split(" ")
            for i, st_ in enumerate(stols_):
                print(f"[i]:[{str(i)}]\n[st_]:[{str(st_)}]")
                if "run" in str(st_):
                    try:
                        rules_ = str(stols_[i+1])
                    except:
                        rules_ = "rules.txt"
                    try:
                        flags_ = str(stols_[i+2])
                    except:
                        flags_ = "svb"
                    self.Li.start_snrokl(rules_, flags_)
                    return "running"

                if "add-rule" in str(st_):
                    print("[Adding Rule]")
                    # Append new rule to 'rules.txt'
                    new_rule = str(stols_[i+1])
                    self.FM.write_file("rules.txt", new_rule, ";\n", "a+")
                    rules_set = self.FM.read_file("rules.txt", ";")
                    ret_msg = f"<br> Rules: <br> "
                    for j, rs in enumerate(rules_set):
                        ret_msg += f"[{str(j)}] >> {str(rs)} <br>"
                    return ret_msg

                if "get-stack" in str(st_):
                    print("Updating User - Collected Data-List")
                    # Read data from 'DATA' folder
                    # -> give options to choose which file to read
                    stack_folder = str(stols_[i+1])
                    stack_list = self.FM.file_list("DATA/")
                    ret_msg = f"<br> StackList: <br> "
                    for k, sl in enumerate(stack_list):
                        ret_msg += f"[{str(k)}] >> {str(sl)} <br>"
                    return ret_msg
                

                if "get-file" in str(st_):
                    stack_folder = str(stols_[i+1])
                    if "rules.txt" in stack_folder:
                        file_data = self.FM.read_file(stack_folder, "\n")
                        rd = str(file_data[0]).replace("\\n", "\n") # Yeah, just leave it like this..
                        crd = rd.replace("', '", " ")
                        ret_msg = f"\
                            <textarea\
                                v-model='message'\
                                cols='80' \
                                rows='2' \
                                style='\
                                    width: 78vw; \
                                    height: 80vh;' \
                                id='da-rules'>\
                                {crd} \
                                \
                            </textarea>"
                        return ret_msg
                    else:
                        print("Updating User - Collected File")
                        # Read data from 'DATA' folder
                        # -> give options to choose which file to read
                        file_data = self.FM.read_file(stack_folder, "\n")
                        ret_msg = f"<br> FileData: <br> "
                        for l, fd in enumerate(file_data):
                            fdd =str(fd).replace("\n", "<br>")
                            ret_msg += f"[{str(l)}] >> {fdd} <br>"
                        return ret_msg




        except Exception as e:
            print(f"[E]:[{str(e)}]")
            return(f"[E]:[{str(e)}]")
            



    async def handle_client(self, websocket, cl_id, msg_, path):
        try:
            print(f'\n~[ClientHandOff]:[{str(cl_id)}]:[{str(websocket)}]')
            print(f"\n~[FROM_CLIENT]:[{str(msg_)}]")
            if "cmd" in str(msg_):
                print(f"[$]:[{str(msg_)}]")
                cmd_ = str(msg_.split("$")[1])
                p = subprocess.Popen(cmd_, stdout=subprocess.PIPE, shell=True)
                out, err = p.communicate()
                sets_ = str(out.decode()).split("\n")
                ret_msg =  f"┌──(NixLyn㉿GPT)-[kali]<br>└─$ {cmd_} <br>"   #"<h4>"+str(cl_id)+"</h4><br>"
                for i, se_ in enumerate(sets_):
                    print(f"[i]:[{str(i)}]::[se_]:[{str(se_)}]")
                    ret_msg += f"[{str(i)}] >> {str(se_)} <br>"
                ret_msg += f"<br>"

            if "node" in str(msg_):
                ret_msg = self.get_cmd(msg_)
                print("Accessing-NODE")

            await self.send_msg(websocket, ret_msg)
        except Exception as e:
            print(f"[E]:[HANDLE_CLIENT]:[{str(e)}]")

    async def new_client_conn(self, client_socket, path):
        """
        Identify New Client Connection
        """
        self.clients.append(client_socket)
        cl_id = len(self.clients)
        print(f"[+]:[NEW CLIENT CONNECTED]:[>{str(path)}<]")
        while True:
            msg_ = await client_socket.recv()
            print(f"[FROM_CLIENT]:[{str(msg_)}]")
            if "[CONN_REQ]" in str(msg_):
                print("[@]:[CONNECTION_REQUEST]")
                await SN.send_msg(client_socket, f"<br>┌──(NixLyn㉿GPT)-[kali]<br>└─$")
            else:
                await SN.handle_client(client_socket, cl_id, msg_, path)

    async def start_server(self):
        """
        Start Endless Server Loop
        """
        print("[WEB_SERVER_STARTED]")
        await websockets.serve(self.new_client_conn, 'localhost', 12345)


if __name__=="__main__":
    SN = SnrokL_Node()
    SN.event_loop = asyncio.get_event_loop()
    SN.event_loop.run_until_complete(SN.start_server())
    SN.event_loop.run_forever()






# NoOOP



SIS= """
 async def send_msg(msg_: str):
    for i, client in enumerate(all_clients):
        print(f'[TO]:[{str(i)}]:[{str(client)}]')
        await client.send(msg_)


async def new_client_conn(client_socket, path):
    all_clients.append(client_socket)
    while True:
        msg_ = await client_socket.recv()
        await send_msg('sis:'+msg_)

async def start_server():
    await websockets.serve(new_client_conn, '127.0.0.1', 8083)

if __name__=="__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(start_server())
    event_loop.run_forever()
"""