import socket
import collections
import numpy as np
import matplotlib.pyplot as plt

#host = 'B8:27:EB:A5:E7:E9'
host = 'E8:B1:FC:F5:16:02'
#host = socket.gethostname()
port = 4

dset = 100
y = collections.deque(np.zeros(dset), maxlen=dset)
x = np.linspace(0, 1, dset+1)[0:-1] # all points from 0 to 1 excluding 1
plotAxis1 = []

backlog = 1
bufferSize = 1024

client = None

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((host, port))
s.listen(backlog)
client, address = s.accept()

plt.style.use('ggplot')

def livePlot(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    # First pass in loop initializes
    if line1 == []:
        # turn on interactive plot
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # plot axis in the figure
        line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)
        plt.ylabel('RSSI')
        #plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

while True:
    cmd = client.send(bytes(input(), 'utf-8'))
    res = client.recv(bufferSize)
    print(res)
    res = str(res, 'utf-8')
    if res == 'quit':
        break
    elif res[0] == 'u':
        val = int(res[1:])
        y.append(val)
        plotAxis1 = livePlot(x, y, plotAxis1)
        #print(val)
        #y.append(int(res[1:]))


print('Closing sockets')
client.close()
s.close()
