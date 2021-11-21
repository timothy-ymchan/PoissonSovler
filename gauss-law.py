import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import h5py
import argparse

# Command line parsing
parser = argparse.ArgumentParser(description='Verification of gauss law')
parser.add_argument('--path',type=str,required=True,help='Path of HDF5 file')

args = parser.parse_args()

# Read file 
f = h5py.File(args.path,'r')

x1,x2 = f['metadata']['domain-size']
N1,N2 = f['metadata']['domain-div']

h = x1/N1
V_n = np.array(f['result']['volt'])[1:-1,1:-1]
Ex,Ey = np.gradient(-V_n)


# Plot background to visualize the region surface used to calculating the flux
fig = plt.figure()
plot = fig.add_subplot(111)

plot.set_aspect(1) 

Y,X = np.meshgrid(np.linspace(0,x2,N2),np.linspace(0,x1,N1))

plot.pcolormesh(X,Y,V_n,shading='nearest',cmap=cm.coolwarm)
plot.quiver(X,Y,Ex,Ey,color='black')


# Verify gauss law
cx, cy = int(N1/2), int(N2/2) # Coordinate of center 
bw, bh = 5,5 # Box width and height

flux = 0
xmin, xmax = int(cx-bw/2)+1, int(cx+bw/2)
ymin, ymax = int(cy-bh/2)+1, int(cy+bh/2)

x1s, x2s = np.linspace(0,x1,N1),np.linspace(0,x2,N2)
plot.plot(x1s[cx],x2s[cy],'o',color='m')
plot.plot(x1s[xmin],x2s[ymin],'o',color='m')
plot.plot(x1s[xmin],x2s[ymax],'o',color='m')
plot.plot(x1s[xmax],x2s[ymin],'o',color='m')
plot.plot(x1s[xmax],x2s[ymax],'o',color='m')

for y in range(ymin+1,ymax): # Flux in x-direction
    flux += Ex[xmax][y]*h
    flux -= Ex[xmin][y]*h
    plot.plot(x1s[xmin],x2s[y],'x',color='orange')
    plot.plot(x1s[xmax],x2s[y],'x',color='orange')

for x in range(xmin+1,xmax): # Flux in y-direction
    flux += Ey[x][ymax]*h
    flux -= Ey[x][ymin]*h
    plot.plot(x1s[x],x2s[ymax],'x',color='g')
    plot.plot(x1s[x],x2s[ymin],'x',color='g')

flux += 0.5*h*(Ex[xmax][ymax] + Ey[xmax][ymax]) # Flux in corners 
flux -= 0.5*h*(Ex[xmin][ymin] + Ey[xmin][ymin])
flux += 0.5*h*(Ex[xmax][ymin] - Ey[xmax][ymin])
flux -= 0.5*h*(Ex[xmin][ymax] - Ey[xmin][ymax])
print(f'Flux calculate: {flux}')



plt.show()