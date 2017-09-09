from __future__ import unicode_literals,print_function

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

from tinydb import TinyDB,where

import math
import time
import sys
import copy

import list_dict_DB;reload(list_dict_DB)
list_dict_DB = list_dict_DB.list_dict_DB

import pandas as pd
import dataset

from tinydb.storages import MemoryStorage
try:
    import simplejson as json
except:
    import json

run = False # True will run, save, and exit. False will plot

######################
def time_dataset_mem():
    try:
        del DF
    except:
        pass

    T0 = time.time()
    db = dataset.connect('sqlite:///:memory:')
    table = db['test_table']
    table.insert_many(data)
    TC = time.time() - T0
    
    T0 = time.time()
    table.find_one(iri=30)
    TQ = time.time() - T0
    
    sys.stdout.write('.');sys.stdout.flush()
    return TC,TQ


def time_pandas():
    try:
        del DF
    except:
        pass

    T0 = time.time()
    DF = pd.DataFrame(data)
    TC = time.time()-T0

    T0 = time.time()
    DF[DF.iri == 30]
    TQ = time.time() - T0
    
    sys.stdout.write('.');sys.stdout.flush()
    return TC,TQ

def time_list_dict_DB():
    try:
        del DB
    except:
        pass

    T0 = time.time()
    DB = list_dict_DB(data)
    TC = time.time()-T0

    T0 = time.time()
    DB[DB.Q().iri == 30]
    TQ = time.time() - T0
    
    sys.stdout.write('.');sys.stdout.flush()
    return TC,TQ

def time_tinyDBmem():
    try:
        del tDB
    except:
        pass

    T0 = time.time()
    tDB = TinyDB(storage=MemoryStorage)
    tDB.insert_multiple(data)
    TC = time.time()-T0

    T0 = time.time()
    tDB.search(where('iri')==30)
    TQ = time.time() - T0
    sys.stdout.write('.');sys.stdout.flush()
    return TC,TQ
    

def time_loop_copy():
        
    T0 = time.time()
    list_data = copy.copy(data)
    TC = time.time()-T0

    T0 = time.time()
    [item for item in list_data if item['iri']==30]
    TQ = time.time() - T0
    
    sys.stdout.write('.');sys.stdout.flush()
    return TC,TQ
######################
    
def compute_averages(arr,name=''):
    mTC = sum(a[0] for a in arr)*1.0/len(arr)
    print('\n{:s} Create Avg (N={:d}): {:0.5e}'.format(name,len(arr),mTC))

    mTQ = sum(a[1] for a in arr)*1.0/len(arr)
    print('{:s} Query Avg (N={:d}): {:0.5e}'.format(name,len(arr),mTQ))
    return {'TC':mTC,'TQ':mTQ}


def test(N=10):
    results = {}
    results['pandas'] = compute_averages([time_pandas() for _ in xrange(N)],name='Pandas')
    results['list_dict_DB'] = compute_averages([time_list_dict_DB() for _ in xrange(N)],name='list_dict_DB')
    results['TinyDB_mem'] = compute_averages([time_tinyDBmem() for _ in xrange(N)],name='tinyDB in memory')
    results['dataset_mem'] = compute_averages([time_dataset_mem() for _ in xrange(N)],name='dataset_mem')
    results['loop_copy'] = compute_averages([time_loop_copy() for _ in xrange(N)],name='loop_copy')
    
    return results

Nds = [int(10.0**(a)) for a in [3,3.5,4,4.5,5,5.5,6]]


if run:
    ###############################
    all_res = []
    for Nd in Nds:
        print(math.log10(Nd))
        data = [{'i':i,'i2':2*i,'ihd':0.5*i,'iri':int(1.0*i**(0.5))} for i in xrange(Nd)]
    
        all_res.append(test())
        print("")


    with open('results.json','w') as F:
        json.dump(all_res,F)
    
    sys.exit()
    #############################

all_res = json.load(open('results.json'))

plt.close('all')
plt.style.use('seaborn-darkgrid')
fig = plt.figure(figsize=(15,4))

axes = [None for _ in range(3)]
axes[0] = plt.subplot2grid((1,5), (0,0), colspan=2)
axes[1] = plt.subplot2grid((1,5), (0,2), colspan=2)
axes[2] = plt.subplot2grid((1,5), (0,4), colspan=1)


shapes = ['-o', '-s', '-D', '-<', '-H']
colors = [[0.36392156862745095, 0.5755294117647058, 0.7483921568627451],
          [0.9152941176470588, 0.2815686274509803, 0.2878431372549019],
          [0.44156862745098036, 0.7490196078431373, 0.432156862745098],
          [1.0, 0.5984313725490196, 0.19999999999999996],
          [0.6768627450980391, 0.4447058823529412, 0.7113725490196078]]

mpl.rcParams['font.size'] = 14
mpl.rcParams['lines.linewidth'] = 2

methods = all_res[0].keys()
methods = [ 'list_dict_DB', 'loop_copy', 'pandas','TinyDB_mem','dataset_mem']
for it,tool in enumerate(methods):
    
    axes[0].plot(Nds,[R[tool]['TQ'] for R in all_res],shapes[it],color=colors[it])
    axes[1].plot(Nds,[R[tool]['TC'] for R in all_res],shapes[it],color=colors[it])
    
    axes[2].plot([],[],shapes[it],color=colors[it],label=methods[it])
    
    print([R[tool]['TQ'] for R in all_res])
for ax in axes[:2]:
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('database size')
    ax.set_ylim([1e-6,1e2])
    ax.set_xlim([10.0**(2.9),10.0**(6.1)])
#     ax.set_aspect('equal',adjustable='box')

axes[1].set_yticklabels([])

axes[0].set_title('Query')
axes[1].set_title('Create')

axes[0].set_ylabel('time (s)')

ax = axes[2]
ax.legend(loc='center',numpoints=1,fontsize=12)
ax.set_frame_on(False)
ax.set_xticks([])
ax.set_yticks([])

fig.tight_layout()
# fig.savefig('benchmark.png')
plt.show()


# Slope at the end
slopeQ = {}
slopeC = {}
for tool in methods:
    Qtime = np.log10([res[tool]['TQ'] for res in all_res[-2:]])
    Qtime = Qtime[-1]-Qtime[-2]
    
    slopeQ[tool] = Qtime/0.5
    
    Ctime = np.log10([res[tool]['TC'] for res in all_res[-2:]])
    Ctime = Ctime[-1]-Ctime[-2]
    
    slopeC[tool] = Ctime/0.5
    
    print('{}|{:0.2f}|{:0.2f}'.format(tool,slopeQ[tool],slopeC[tool]))







