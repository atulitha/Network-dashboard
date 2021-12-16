import csv
import codecs
from datetime import datetime
import multiprocessing
Pool = multiprocessing.Pool
# Global lock
global_lock = multiprocessing.Lock()
file_contents = []
hd = dict  # global variable


def writedevicelist(dev):
    """
    This function writes a list of devices that are returned by conn function
    :param dev: dictionary value to write the device that is passed for conn() function
    :return: nothing
    """
    import json
    global_lock.acquire()
    with open('devicelist.json', mode='a+') as file:
        for hd in dev:
            x = json.dumps(hd, indent=4)
            file.write(x + "\n")
    global_lock.release()


def writetxt(gdata):
    """
    This function writes data to file results.txt
    :param gdata: The result from execution of command in conn() current device that connected and command-executed
    command-executed in current connection
    :return: nothing
    """
    import os
    #  from datetime import datetime
    global_lock.acquire()
    #  start_time = datetime.ctime(datetime.now())
    for sl in gdata:
        dev, cmd, data = sl
        filename = str("multiple/")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename+str(dev)+".txt", mode='w+', encoding='utf-8-sig') as f:
            f.write("\n" + "*" * 30 + str(dev) + "*" * 30 + "\n\n")
            f.write(cmd + "\n\n" + data + "\n\n")
    global_lock.release()


def singlefile(gdata2):
    global_lock.acquire()
    filename = "single/"
    res = list(filter(None, gdata2))
    print(res)
    import os
    with open(filename + "all.csv", mode='w+', encoding='utf-8-sig') as f:
        fieldnames = ['hostname / IP address', 'Command', 'output']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dev_list, cmd_out in res:
            for sl in cmd_out:
                dev, cmd, data = sl
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                writer.writerow({'hostname / IP address': str(dev), 'Command': cmd, 'output': data})
    global_lock.release()


def writeerror(data, hd):
    """
    writes error to result file
    :param data: reads error when conn()
    :param hd: details of current device
    :return: nothing
    """
    global_lock.acquire()
    with open('errors.txt', mode='a+', encoding='utf-8-sig') as f:
        f.write("\n" + "*" * 30 + hd["host"] + "*" * 30 + "\n\n")
        f.write(str(data) + "\n\n")
        f.write(hd["device_type"] + "\n\n")

    with open("errors.csv", mode='a+', encoding='utf-8-sig') as f:
        f.write(hd["host"] + "," + "Not Connected\n")
    global_lock.release()


def readcmd():

    with open("cmd.txt", 'r') as f:
        host_cmd_var = f.read()
        host_cmd_array = host_cmd_var.splitlines()
        # Removes any empty arrays
        host_cmd_array = list(filter(None, host_cmd_array))
        # Removes leading/trailing spaces
        host_cmd_array = list(map(str.strip, host_cmd_array))
        # print("list of commands are"+str(host_cmd_array))
        return host_cmd_array


def csvread():
    """
    Reads the list of Internet protocol address from data.csv file
    :return:
    """
    import csv
    with codecs.open('data.csv', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        return rows


cmd = readcmd()


def runt(hd):
    from netmiko import SSHDetect, Netmiko
    output = list()
    start_time = datetime.now()
    try:
        guesser = SSHDetect(**hd)
        best_match = guesser.autodetect()
        hd["device_type"] = best_match
        print(best_match)
        connection = Netmiko(**hd)
        print(connection.find_prompt())
        print("\ntook for connecting: " + str(datetime.now() - start_time))
        start_time = datetime.now()

        if len(cmd) == 0:
            print("enter command after > prompt press 0 to end the list")
            while True:
                x = input("> ")
                if x == '0':
                    break
                else:
                    cmd.append(x)
                    print(cmd)
        print("list of commands are" + str(cmd))
        try:
            for c in cmd:
                 if c == "config":
                     c_list = []
                     while c !==end:
                         c_list.append(c)
                     out = connection.send_config_set(config_commands=c_list)
                 else:
                print("executing: " + c)
                #resultx = connection.enable()
                #print("enable result:")
                #print(resultx)
                out = connection.send_command(c, delay_factor=1.0)
                print(out + "\n\n")
                output.append([hd['host'], c, out])
        except:
            output.append([hd['host'], c, out])
            pass
        print("\ntook for executing list of commands: " + str(datetime.now() - start_time))
        connection.disconnect()
        writetxt(output)
        hd.pop('password')
        hd.pop("secret")
        return hd, output
    except Exception as e:
        hd["device_type"] = "Not connected"
        print(e)
        writeerror(e, hd)
    finally:
        print("process took: " + str(datetime.now()-start_time))


def inputval():
    """
    reads inputs and sends to connection
    :return: Nothing
    """
    user = 'abhinava.rallapalli' # input("enter username for this session: ")
    password = 'Sudoadmin@123'  # input("enter password for this session: ")
    iplist = csvread()

    dev = []
    if user != "root":
        for ip in iplist:
            ip = str(ip)
            ip = ip.replace("[", '').replace("]", '').replace("'", '', 2)
            hd = {
                "device_type": "autodetect",
                "host": str(ip),
                "username": user,
                "password": password,
                "secret": password,
                "global_delay_factor": 10.0,}
            dev.append(hd)
    return dev


data1 = inputval()
if __name__ == '__main__':
    start_time = datetime.now()
    with open("errors.csv", mode='w+', encoding='utf-8-sig') as f:
        fieldnames = ['hostname / IP address', 'Status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    if len(data1) > 60:
        nprocs = 60
    else:
        nprocs = len(data1)
    with Pool(nprocs) as p:
        data2= p.map(runt, data1)

    print(data2, sep=", ")

    # writedevicelist(data2)
    singlefile(data2)

    print('total time is: ' + str(datetime.now()-start_time))