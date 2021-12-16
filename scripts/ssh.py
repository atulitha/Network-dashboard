
def inputvar(host, command1, command2=None, command3=None):
    iplist = host.split()
    cmd = command1.split(",")
    config = command2.split(",")
    cmd3 = command3.split(",")
    user = 'EntPrime' # input("enter username for this session: ")
    password = 'leg2REAM!!'  # input("enter password for this session: ")
    dev = []
    for ip in iplist:
        hd = {
                    "device_type": "autodetect",
                    "host": str(ip),
                    "username": user,
                    "password": password,
                    "secret": password,
                    "global_delay_factor": 1.0,
                    "cmd": cmd,
                    "config": config,
                    "cmd3": cmd3
        }
        dev.append(hd)
    #print(hd['cmd'])
    return dev
    
def runt(hd):
    from netmiko import SSHDetect, Netmiko
    from datetime import datetime
    output = list()
    out = list()
    writeerror = list()
    start_time = datetime.now()
    cmd = hd['cmd']
    config = hd["config"]
    cmd3 = hd["cmd3"]
    hd.pop('cmd')
    print(cmd)
    hd.pop("config")
    print(cmd)
    hd.pop("cmd3")
    print(cmd)

    try:
        connection = Netmiko(**hd)
        print(connection.find_prompt())
        print("\ntook for connecting: " + str(datetime.now() - start_time))
        start_time = datetime.now()
        if config is None:
            try:
                for c in cmd:
                    print(c)
                    print("executing: " + c)
                    out = connection.send_command(c, delay_factor=1.0)
                    print(out + "\n\n")
                    output.append([hd['host'], c, out])
            except Exception as e:
                print(e)
                output.append([hd['host'], c, out])
                pass
        else:
            try:
                for c in cmd:
                    print(c)
                    print("executing: " + c)
                    out = connection.send_command(c, delay_factor=1.0)
                    print(out + "\n\n")
                    output.append([hd['host'], c, out])
                cout= connection.send_config_set(config)
                print(cout)
                output.append(['-'*5, config, '-'*5, cout])
                for c in cmd3:
                    print(c)
                    print("executing: " + c)
                    aout= connection.send_command(c, delay_factor=1.0)
                    print(out + "\n\n")
                    output.append([hd['host'], c, aout])
            except Exception as e:
                print(e)
                output.append([hd['host'], c, out])
                pass
        print("\ntook for executing list of commands: " + str(datetime.now() - start_time))
        connection.disconnect()
        return hd, output
    except Exception as e:
        output.append([hd['host'], e, out])
        print(e)
        return output
    finally:
        print("process took: " + str(datetime.now()-start_time))