import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import h5py
import argparse

# Command line parsing
parser = argparse.ArgumentParser(description='Visualization tool for Lab 6')
parser.add_argument('--path',type=str,required=True,help='Path of HDF5 file')
gp = parser.add_mutually_exclusive_group(required=True)
gp.add_argument('--field',help='Visualize electric field',action='store_true')
gp.add_argument('--pot',help='Visualize potential',action='store_true')
gp.add_argument('--rho',help='Visualize charge distribution',action='store_true')

args = parser.parse_args()


# Read file 
f = h5py.File(args.path,'r')

x1,x2 = f['metadata']['domain-size']
N1,N2 = f['metadata']['domain-div']
v_top,v_bottom,v_left,v_right = f['metadata']['BCs']

# Print basic information
print('Description:')
print(f'Domain size (x1,x2): ({x1},{x2})')
print(f'Domain div  (N1,N2): ({N1},{N2})')
print(f'Boundary conditions (top,bot,left,right): ({v_top},{v_bottom},{v_left},{v_right})')

# Plotting
if args.pot:
    V_n = f['result']['volt']
    fig = plt.figure()
    plot = fig.add_subplot(111,projection='3d')

    X,Y = np.meshgrid(np.linspace(0,x1,N1+2),np.linspace(0,x2,N2+2))
    plot.plot_surface(X,Y,V_n,cmap=cm.coolwarm,antialiased=True)

    plt.show()

    f.close()

if args.rho:
    rho = f['result']['rho']
    fig = plt.figure()
    plot = fig.add_subplot(111)

    X,Y = np.meshgrid(np.linspace(0,x1,N1),np.linspace(0,x2,N2))
    im = plot.pcolormesh(X,Y,rho,cmap=cm.coolwarm,shading='nearest')
    fig.colorbar(im)

    plt.show()


if args.field:
    h = x1/N1
    V_n = np.array(f['result']['volt'])[1:-1,1:-1]
    Ey,Ex = np.gradient(-V_n)

    fig = plt.figure()
    plot = fig.add_subplot(111)

    plot.set_aspect(1)
    

    X,Y = np.meshgrid(np.linspace(0,x1,N1),np.linspace(0,x2,N2))
    """E = np.sqrt(Ex**2 + Ey**2) # Rescalign code
    Euq = np.quantile(E.flat,0.5)
    Ex = (Ex/E)*Euq*np.tanh(np.abs(Ex)/Euq)
    Ey = (Ey/E)*Euq*np.tanh(np.abs(Ey)/Euq)"""

    plot.pcolormesh(X,Y,V_n,shading='nearest',cmap=cm.coolwarm)
    plot.streamplot(X,Y,Ex,Ey,color='black')

    plt.show()

    

