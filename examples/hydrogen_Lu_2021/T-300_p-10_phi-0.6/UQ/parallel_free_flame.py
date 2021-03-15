import numpy as np
from mpi4py import MPI
from pyutils.ctutils.driver.chem_uq import free_flame
import matplotlib.pyplot as plt

# parallel init
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = 500

sl, dl = free_flame(n, 'H2', T=300, p=1013250., phi=0.6)

# data collection
sendbuf = sl
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, n])
comm.Gather(sendbuf, recvbuf, root=0)
sl_all = recvbuf

sendbuf = dl
recvbuf = None
if rank == 0:
    recvbuf = np.empty([size, n])
comm.Gather(sendbuf, recvbuf, root=0)
dl_all = recvbuf

if rank == 0:
    np.savez('free_flame', sl=sl_all.flatten(), dl=dl_all.flatten())

"""
if rank == 0:
    print(sl_all)
    print(dl_all)
    plt.scatter(dl_all, sl_all)
    plt.savefig('fig_test.png')
"""
