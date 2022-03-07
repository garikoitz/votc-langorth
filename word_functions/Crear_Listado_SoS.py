#!/bcbl/home/home_g-m/glerma/software/Anaconda/bin python
# -*- coding: UTF-8 -*-
# File    : Crear_Listado_SoS.py
# Author  : Garikoitz Lerma-Usabiaga garikoitz@gmail.com
# Version : 0.2, Date    : 12.11.2014
# Version : 0.3, Date    : 5.3.2022
# Usage   : With a given SoS formated (| for data type and tab separated) word
#           database, read it and remove not desired words, then stablish the
#           hard constraints (in this case lenght) and then create the
#           populations, in this case high and low frequencies. Then run the
#           matlab script (it has to have the soft constraints and other options
#           in the same .m script).
#           Run this file as it is without any input arguments and it will
#           output the sampleXXX.txt files to be loaded in the presentation
#           programs as it is.
# Todo    : 1.-
#           2.-
# Load required packages
import pandas as pd
import subprocess as sp
import os

repopath = '~/toolboxes/votc-langorth'
join = os.path.join

# Aplicar a espal_orig.txt antes de hacer cualquier cambio
# iconv -t UTF-8 -f ISO-8859-1 espal_orig.txt > espal_orig_utf8.txt
# Ademas para saber la codificacion usar file -bi filename.txt

# Ademas quitar las palabras malsonantes que tengan tilde y enye a mano, no he
# conseguido quitarlos a traves del codigo por culpa de la codificacion en el
# codigo

# OJO: en este listado ya hay palabras que he revisado que no tienen cognados,
# y ademas tienen informacion de concretness. Hay que variar el tema de las frecuencias,
# pero haciendo eso ya tengo los listados de palabras que queriamos
words = pd.read_table(join(repopath,'DATA','Espal456SinCognados_SinConcreteness_UTF8.txt'), encoding='utf-8', sep='\s+')
# del words['bim']

# Nos quedamos solo con aquellas columnas que nos interesan (segun que leemos
# usar una cosa u otra)
# Paso del concreteness, ya que me quita demasiadas palabras y nadie lo usa
# espalcols = ['word', 'num_letters', 'frq', 'concreteness', 'Lev_N',
#              'pos_tok_SBOF']
# espalcols = ['word', 'num_letters', 'frq', 'Lev_N', 'pos_tok_SBOF']
# wordscols = words[espalcols]
wordscols = words
# Le damos nombres los nombres que nos interesan (si hace falta)
# renameit = ['word', 'nlet', 'frq', 'conc', 'Lev', 'bi']
# renameit = ['word', 'nlet', 'frq', 'Lev', 'bi']
# wordscols.columns = renameit

# No todas las palabras tienen info de concretness, quitar las que no tienen
# esta informacion: reduce la bbdd de 244K a 6.6K, y ya hace dificil encontrar
# suficientes palabras.
# wordsconc = wordscols.query("conc != '\N'")
wordsconc = wordscols
# Listado de palabras que vamos eliminando una vez vistos los resultados
# Las palabras con enye o tilde quitarlas en espal_orig_utf8_limpio.txt
words_limpio = wordsconc.query("word != [" +
    "'caca', 'moro', 'seno', 'tonto', 'culo', 'race', 'guarra', " +
    "'puta', 'matar', 'sexo', 'boba', 'loca', " +
    "'coito', 'harry', 'chicos', 'temo', 'lanka', " +
    "'mudara', 'brahms', 'hakim', 'stones', 'babu',"+
    "'chupo', 'TRUE', 'lupin', 'jockey', 'kosovo'," +
    "'zurich', 'selma', 'dani', 'muchas', 'david'," +
    "'miren'"
    "]")

# Hard constraint: only use num_letters of 4 and 5
words456 = words_limpio[(words_limpio.nlet == 4) | (words_limpio.nlet == 5)
                       | (words_limpio.nlet == 6)]

words456 = words_limpio

# Write it as excel in order to remove it using E-Hitz any word with basque frequency
# differetn to 0 and number of neighbours different to 0
# words456.to_csv('words456_EHITZ_antes_iso8859.txt',index=False,encoding='ISO-8859-1',sep='\t')


# Y creamos dos grupos, los de alta y baja frequencia para meter a SOS
words456LF = words456.loc[(words456.frq >= .5)
                        & (words456.frq <= 5), :]
words456HF = words456.loc[(words456.frq >= 50)
                        & (words456.frq <= 500), :]
# len(words456LF)
# len(words456HF)

# Antes de escribirlo le damos formato a las columnas segun quiere SoS
formateado = ['word|s', 'nlet|f', 'frq|f', 'Lev|f', 'bi|f']
# formateado = ['word|s', 'nlet|f', 'frq|f', 'conc|f', 'Lev|f', 'bi|f']
words456LF.columns = formateado
words456LF.to_csv('espal456LF.txt', index=False, encoding='utf-8', sep='\t')
words456HF.columns = formateado
words456HF.to_csv('espal456HF.txt', index=False, encoding='utf-8', sep='\t')

# Ahora lanzamos el script de SoS con las opciones que estan en el script .m,
# editar el script para cambiar las opciones de creacion de samples
cmd = str('matlab -nojvm -nodesktop -r "run /bcbl/home/home_g-m/glerma/00local/CODE/MATLAB/SoS_VWFA.m"')
spcmd = sp.call(cmd, shell=True)


# Lo de abajo tener comentado, voy a mirar cuales son las palabras que ya tengo
# y las que tengo que generar de nuevo
# Bueno igual no, igual creo una nueva version de todo, ya uq eahora las listas
# no tienen porque tener las mismas palabras.
# El output de Matlab se llama:
soslist_RWLF1 = pd.read_table('RW_LF1Length456_80.txt', encoding='utf-8', sep='\t')
soslist_RWLF2 = pd.read_table('RW_LF2Length456_80.txt', encoding='utf-8', sep='\t')
soslist_RWHF1 = pd.read_table('RW_HF1Length456_80.txt', encoding='utf-8', sep='\t')
soslist_RWHF2 = pd.read_table('RW_HF2Length456_80.txt', encoding='utf-8', sep='\t')

del soslist_RWLF1['Unnamed: 5']
del soslist_RWLF2['Unnamed: 5']
del soslist_RWHF1['Unnamed: 5']
del soslist_RWHF2['Unnamed: 5']

