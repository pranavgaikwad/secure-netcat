import select, socket, sys, Queue

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 50001))
client.setblocking(0)

inputs = [client, sys.stdin]
outputs = []
data_to_send = []

while inputs:
    try:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is sys.stdin:
                data = sys.stdin.readline()
                if not data:
                    break
                print 'entered data  ', data
                data_to_send.append(data)
                print data_to_send
            elif s is client:
                data = s.recv(1024)
                if data:
                    print data
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    sys.exit(1)
            else:
                pass

        for s in exceptional:
            # print '__exceptional__'
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            sys.exit(1)

        if len(data_to_send) > 0:
            client.send(data_to_send[0])
            data_to_send = []

    except (EOFError, KeyboardInterrupt):
        client.close()
        break