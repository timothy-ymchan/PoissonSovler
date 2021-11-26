import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import argparse
import glob
import h5py 

def main():
    args = parse_args()
    print(args.hdf5_glob)
    hdf5_path = sorted(list(glob.glob(args.hdf5_glob))) # Get the paths

    hs = np.zeros(len(hdf5_path))
    error = np.zeros(len(hdf5_path))

    for idc, path in enumerate(hdf5_path):
        hdf5 =  h5py.File(path,'r')
        domain_div = np.array(hdf5['metadata']['domain-div'])
        domain_size = np.array(hdf5['metadata']['domain-size'])

        print(path,domain_div,np.array(hdf5['metadata']['eps']))
        
        h = (domain_size/domain_div)[0]

        X,Y,V_anal = analytical_solution(domain_size,domain_div)
        V_num = hdf5['result']['volt']

        #fig = plt.figure()
        #ax = fig.add_subplot(111,projection='3d')
        #ax.plot_surface(X,Y,V_num,cmap=cm.plasma,antialiased=True,alpha=1)
        #ax.plot_surface(X,Y,V_anal+2,cmap=cm.plasma,antialiased=True,alpha=1)

        hs[idc] = h
        error[idc] = np.mean(np.abs((V_anal-V_num)))
        #plt.show()
    
    m,c = np.polyfit(np.log10(hs), np.log10(error), 1)
    plt.title('Error vs h')
    plt.xlabel(r'$\log_{10} h$')
    plt.ylabel(r'$\log_{10} |V_{true} - V_{numeric}|$')
    plt.plot(np.log10(hs),np.log10(error),'o')
    plt.plot(np.log10(hs),m*np.log10(hs)+c,'-',label=f'y={m:.3f}x+{c:.3f}')
    plt.legend()
    plt.show()
    


def analytical_solution(domain_size,domain_div):
    x1,x2 = domain_size
    N1,N2 = domain_div

    coord_x = lambda x: (x/(N1+1))*x1
    coord_y = lambda y: (y/(N2+1))*x2

    X,Y = np.meshgrid(np.linspace(0,x1,N1+2),np.linspace(0,x2,N2+2))
    V = np.zeros(shape=(N1+2, N2+2))

    for i1 in range(0,N1+2):
        for i2 in range(0,N2+2):
            x,y = coord_x(i1),coord_y(i2)
            V[i1][i2] = np.sinh(2*np.pi*y)*np.sin(2*np.pi*x)/np.sinh(2*np.pi)
    
    return X,Y,V


def parse_args():
    parser = argparse.ArgumentParser(description='Convergence Test')
    parser.add_argument('--hdf5-glob',type=str,required=True,help='HDF5 Glob')

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()