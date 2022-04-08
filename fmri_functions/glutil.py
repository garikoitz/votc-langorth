#!/bcbl/home/home_g-m/glerma/software/Anaconda/bin python
# -*- coding: UTF-8 -*-
# File    : glutil.py
# Author  : Garikoitz Lerma-Usabiaga garikoitz@gmail.com
# Version : 0.1
# Date    : 12.12.2014
# Usage   :
# Todo    : 1.-
#           2.-
# Devuelve un list con la misma longitud de a diciendo cuantas ocurrencias ha
# encontrado en b. OJo, solo devuelve el index del primero que encuentra. Si
# hay mas de una ocurrencias las ignora

# debuging:
# a = 'lB2'
# b = ['lB1', 'lB1', '1PCAlh', '2PCAlh', 'Acqu']
# b = ['lB1', 'lB2', '1PCAlh', '2PCAlh', 'lB2']
# ismember(a, b)
def fsl2mrtrixb(bvalpath, bvecpath, mrtrixDir=None):
    import numpy as np
    import os
    # bvalpath       = '/Users/glerma/Documents/STANFORD_PROJECTS/NF1_OR/C84/dwi_aligned_trilin_noMEC.bvals'
    # bvecpath       = '/Users/glerma/Documents/STANFORD_PROJECTS/NF1_OR/C84/dwi_aligned_trilin_noMEC.bvecs'
    # mrtrixDir  = '/Users/glerma/Documents/STANFORD_PROJECTS/NF1_OR/C84/dti25trilin/mrtrix/'

    # DEBUG
    # print(bvalpath,bvecpath,mrtrixDir)
    if mrtrixDir is None:
        mrtrixDir = os.getcwd()

    bval = np.loadtxt(bvalpath)
    bvec = np.loadtxt(bvecpath)
    if bvec.shape[0] != 3:
        raise IOError('bvec file should have three rows')
    if bval.ndim != 1:
        raise IOError('bval file should have one row')
    if bval.shape[0] != bvec.shape[1]:
        raise IOError('the gradient file and b value fileshould'
                      'have the same number of columns')

    # Do the calculation
    mrtrixb    = np.append(bvec.transpose(),bval.transpose().reshape(len(bval),1),1)

    # Write it to file
    (head1,tail1) = os.path.split(bvalpath)
    (head2,tail2) = os.path.split(bvecpath)
    (base1,ext) = os.path.splitext(tail1)
    (base2,ext) = os.path.splitext(tail2)
    if base1 != base2:
        raise IOError('bval and bvec file have different base name')

    # Check if we received a folder name or the complete file name.
    (head,tail) = os.path.split(mrtrixDir)
    (base,ext) = os.path.splitext(mrtrixDir)
    if ext:
        mrtrixName = mrtrixDir
    else:
        mrtrixName = os.path.join(mrtrixDir, base1+'.b')
    # Save it
    np.savetxt(mrtrixName, mrtrixb)
    # Return the name of the file that has been written
    return mrtrixName



def createHemiMaskFromAseg(asegFile):
    import os
    import nibabel as nib
    import numpy as np
    # Read the aseg file
    aseg = nib.load(asegFile)
    asegData = aseg.get_data()
    # Read the Look up table
    fLUT = open(os.path.join(os.getenv('FREESURFER_HOME'),'FreeSurferColorLUT.txt'),'r')
    LUT = fLUT.readlines()
    fLUT.close()
    cleanLUT = [s for s in LUT if not '#' in s]
    # Obtain the labels per each hemi
    leftLUT  = [int(s.split()[0]) for s in cleanLUT if 'Left' in s]
    rightLUT = [int(s.split()[0]) for s in cleanLUT if 'Right' in s]
    # Create the two hemispheres
    leftMask   = nib.Nifti1Image(np.isin(asegData, leftLUT), aseg.affine, aseg.header)
    rightMask  = nib.Nifti1Image(np.isin(asegData, rightLUT), aseg.affine, aseg.header)
    # Write the new niftis
    (head,tail) = os.path.split(asegFile)
    nib.save(leftMask, os.path.join(head,'lh.AsegMask.nii.gz'))
    nib.save(rightMask, os.path.join(head,'rh.AsegMask.nii.gz'))
    print('Created ?h.AsegMask.nii.gz in the same folder as the input file')

def ismember(a, b):
    bind = []
    for i, elt in enumerate(b):
        if a == elt:
            bind.append(i)
    if bind == []:
        return 0
    else:
        return bind

# Recibir un dataframe enorme con una unica col llamada orig y devolver
# dataframe para cada condicion qeu se le pase
def gen_rnd_png_list_per_cond(df, cond_dict):
    import numpy as np
    # Genero el listado de archivos cada vez y randomizado para que sea
    # diferente cada vez que generamos un archivo
    pngs = dict()
    for c in sorted(cond_dict.keys()):
        pngs[c] = df[df.orig.str.startswith(c)]
        pngs[c] = pngs[c].reindex(np.random.permutation(pngs[c].index))
    return pngs


def dirCreateCheck(dir_name, check, vb):
    import os, sys, shutil
    print('Will create folder ' + dir_name)
    if check:
        print('check = true')
        if not os.path.isdir(dir_name):
            print('Folder does not exist')
            try:
                os.mkdir(dir_name)
                print('Created ' + dir_name)
                return True;
            except:
                return False
        else:
            sys.exit(dir_name + ' folder exists and you may overwrite it, ' +
                 'rename/delete the folder')
    else:
        try:
            os.mkdir(dir_name)
            return True;
        except:
            return False
