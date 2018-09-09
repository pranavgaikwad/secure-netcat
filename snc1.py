import select, socket, sys, Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setblocking(0)
server.bind(('localhost', 50001))
server.listen(5)

inputs = [server, sys.stdin]
outputs = []
data_to_send = []

while inputs:
    try:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
            elif s is sys.stdin:
                print 'reading mode'
                data = sys.stdin.readline()
                if not data:
                    break
                data_to_send.append(data)
            else:
                data = s.recv(1024)
                if data:
                    l = []
                    l.append(data)
                    print l
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    sys.exit(1)
        
        for s in writable:
            if len(data_to_send) > 0:
                s.send(data_to_send[0])
                data_to_send = []
        
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            sys.exit(0)
    except (EOFError, KeyboardInterrupt):
        server.close()
        break