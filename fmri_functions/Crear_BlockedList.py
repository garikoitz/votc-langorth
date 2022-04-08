# -*- coding: UTF-8 -*-
# File    : Crear_BlockedList.py
# Author  : Garikoitz Lerma-Usabiaga garikoitz@gmail.com
# Version : 0.2 (12.Jan.2015): 
#           En prueba dentro de scanner vi que la task no se actualizaba o
#           randomizaba como tiene que ser
#
#           0.3 (6.April.2022): 
#           Edited to be used in votc-langorht project
#
# Usage   : Edit your variables and run the file from iPython or directly
# Todo    : 1.-
#           2.-
#
# Housekeeping, delete everything before starting
# %reset 

# Load required packages
import os   
# from ismember import ismember
import pandas as pd
import random
# import subprocess as sp
import numpy as np
import glob as glob
# import matplotlib.pyplot as plt
# import csv
import copy

###############################################################################
# FUNCTION DEFINITION
def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

join = os.path.join

def gen_rnd_png_list_per_cond(df, cond_dict,lang):
    # Genero el listado de archivos cada vez y randomizado para que sea
    # diferente cada vez que generamos un archivo
    pngs = dict()
    for c in sorted(cond_dict.keys()):
        pngs[c] = df[df.orig.str.startswith(lang+'_'+c)]
        pngs[c] = pngs[c].reindex(np.random.permutation(pngs[c].index))
    return pngs


def ismember(a, b):
    # Devuelve un list con la misma longitud de a diciendo cuantas ocurrencias ha
    # encontrado en b. OJo, solo devuelve el index del primero que encuentra. Si hay
    # mas de una ocurrencias las ignora
    bind = {}
    for i, elt in enumerate(b):
        if elt not in bind:
            bind[elt] = i
    return [bind.get(itm, None) for itm in a]

###############################################################################
# Folder management
base    = "/Users/glerma/Documents/BCBL_PROJECTS/2022 votc-langorth (Kepa, Manolo)"
workdir = join(base, 'Stimuli', 'blocked')
ensure_dir(workdir)
os.chdir(workdir)
pngdir  = join(base, 'images')

###############################################################################
# MAIN VARIABLES
# Hasta ahora: 
# num_runs = 3
# num_contrabalanceo = 2
# num_orderings = 9
# # condition names and the number of items per run
# conds = {'RW_HF': (1, 60), 'RW_LF': (2, 60), 'PW': (3, 60), 'CS': (4, 60),
#          'PS': (5, 60), 'SD': (6, 60), 'CB': (7, 60), 'FF': (8, 60),
#          'PF': (9, 60), 'FC': (10, 60), 'TASK': (0, 60)}
# items_in_block = 10
# blocks_per_ConditionAndRun = 2
# blocks_per_cond = 6
# name_sufix = ''

# Cambio cuando hemos decidido cambiar los tiempos de mostrar y los TR
langs = {'EN', 'ES', 'EU', 'ZH'}

for lang in langs: 
    print('Now working with language: '+ lang)

    num_runs = 2
    num_contrabalanceo = 2
    num_orderings = 9
    
    # condition names and the number of items per run
    ipc = 80  # Items Per Condition
    conds = {'RW': (1, ipc), 'PW': (2, ipc), 'CS': (3, ipc),
             'PS': (4, ipc), 'SD': (5, ipc), 'CB': (6, ipc), 'FF': (7, ipc)}
             # 'PF': (9, ipc), 'FC': (10, ipc), 'TASK': (0, ipc)}
    items_in_block = 20
    blocks_per_ConditionAndRun = 2
    blocks_per_cond = 4
    name_sufix = 'v01'
    
    
    
    
    # Read all stimuli names
    os.chdir(pngdir)
    pngFileList     = sorted(glob.glob(lang+'*.png'))
    taskPngFileList = sorted(glob.glob('TASK_'+lang+'*.png'))
    os.chdir(workdir)
    print('Found ' + str(len(pngFileList)) + ' files with language ' + lang)
    
    # Convert to DataFrame and separate in conditions
    dfpngs = pd.DataFrame(pngFileList, columns=['orig'])
    
    # Create block lists
    bloques = dict()
    blockPNGlist = items_in_block * ['NA.png']
    condpng = dict()
    for c in conds: condpng[c] = copy.deepcopy(blockPNGlist)
    for order in range(1, num_orderings + 1):
        for nc in range(1, num_contrabalanceo + 1):
            for nr in range(1, num_runs + 1):
                bloques['O'+str(order)+'CB'+str(nc)+'R'+str(nr)+'A'] = (
                             order, nc, nr, 'A', copy.deepcopy(condpng))
                bloques['O'+str(order)+'CB'+str(nc)+'R'+str(nr)+'B'] = (
                             order, nc, nr, 'B', copy.deepcopy(condpng))
    
    for order in range(1, num_orderings + 1):
        for nc in range(1, num_contrabalanceo + 1):
            # Genero el listado randomizado por cada condition y para los 
            # task, y el script lo irá cogiendo
            dictpngs = gen_rnd_png_list_per_cond(dfpngs, conds, lang, nc)    
            # Y ahora empiezo el loop para los runs 
            d = 0   
            for nr in range(1, num_runs + 1):
                # Rellenamos cada uno de los bloques
                for n in ['A', 'B']:
                    llave = 'O'+str(order)+'CB'+str(nc)+'R'+str(nr)+n
                    for c in bloques[llave][4]: 
                        # print order, nc, nr, n, d, c, 'Llave: ', llave
                        if c == 'PF' or c == 'FC' or c == 'TASK':
                            avail = dictpngs[c]
                            short = avail.iloc[range(d, d + items_in_block)]
                        else:
                            avail = dictpngs[c][dictpngs[c].orig.str.contains(str(nc))]
                            short = avail.iloc[range(d, d + items_in_block)]
                        bloques[llave][4][c] = short    
                    d += items_in_block
    
    # Ahora que ya tenemos todos los bloques creados hay que randomizarlos, meterles
    # el task randomizado y luego escribirlo en fichero. Para no liarlo mucho creo 
    # otro loop para esta tarea
    for order in range(1, num_orderings + 1):
        dictpngs = gen_rnd_png_list_per_cond(dfpngs, conds)
        for nc in range(1, num_contrabalanceo + 1):
            for nr in range(1, num_runs + 1):
                # Obtenemos los bloques que vamos a escribir.
                Todasllaves = pd.DataFrame(bloques.keys(), columns = ['llave'])
                rndind = Todasllaves.llave.str.startswith(
                                            'O'+str(order)+'CB'+str(nc)+'R'+str(nr))
                ParaRandomizar = Todasllaves[rndind]
                bloqrnd = dict()
                ind = 0
                for pr in ParaRandomizar.llave.values:
                    for c in conds:
                        if c != 'TASK':
                            ind += 1
                            bloqrnd[ind] = copy.deepcopy(bloques[pr][4][c])
                rndind = bloqrnd.keys()
                random.shuffle(rndind)
                # Ahora metemos las TASK al final, 7 con 0 Tasks, 6 con 1 Task, y 
                # 7 con 2 tasks = 20 tasks por RUN. 
                ind2 = 0
                for r in rndind:
                    ind2 += 1
                    if ind2 >= 8 and ind2 <= 13:
                        cond = bloqrnd[r].orig.iloc[0][0:2]
                        inditem = dictpngs['TASK'].orig.str.startswith('TASK_'+cond)
                        #Select a random item and append it
                        rdit = random.sample(xrange(89), 1) 
                        item = copy.deepcopy(dictpngs['TASK'][inditem].iloc[rdit])
                        bloqrnd[r] = bloqrnd[r].append(item)
                    if ind2 >= 14:
                        cond = bloqrnd[r].orig.iloc[0][0:2]
                        inditem = dictpngs['TASK'].orig.str.startswith('TASK_'+cond)
                        #Select a random item and append it
                        rdit = random.sample(xrange(89), 2)
                        items = copy.deepcopy(dictpngs['TASK'][inditem].iloc[rdit])
                        bloqrnd[r] = bloqrnd[r].append(items)
    
                # Aqui escribiremos los resultados intercalando el rest
                PresFileName = str(lang + '_BLOCK-' + name_sufix +  
                                   '_Order-' + str(order) + 
                                   '_CB-' + str(nc) + '_Run-' + str(nr) + '.txt')
                if os.path.isfile(PresFileName): os.remove(PresFileName)
                PresFile = open(PresFileName, 'a')
                rndind2 = bloqrnd.keys()
                random.shuffle(rndind2)
                for r in rndind2:
                    for w in bloqrnd[r].orig:
                        if w[0:2]   == 'TA': condnum = conds[w[0:4]][0]
                        elif w[0:2] == 'RW': condnum = conds[w[0:5]][0]
                        else               : condnum = conds[w[0:2]][0]
                        PresFile.write(w + '\t' + str(condnum) + '\n')
                    PresFile.write('rest.png'    + '\t' + '17' + '\n')
                    PresFile.write('endrest.png' + '\t' + '18' + '\n')
                PresFile.write('endrest.png'    + '\t' + '18' + '\n')
                PresFile.write('endrest.png'    + '\t' + '18' + '\n')
                PresFile.write('endrest.png'    + '\t' + '18' + '\n')

