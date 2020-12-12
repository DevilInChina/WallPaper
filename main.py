
import matplotlib.image as mpimg
import numpy as np
import sys
from scipy.sparse import csr_matrix
import os
def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

class CSR:
    def __init__(self,dense_matrix):
        self.csr=csr_matrix(dense_matrix)

    def __bytes__(self):
        return self.csr.__bytes__()

    def tostr(self):
        ret = "%%MatrixMarket matrix coordinate real general\n"
        ret +=str(self.csr.shape[0])+" "+str(self.csr.shape[1])+" "+str(len(self.csr.data) )+"\n"
        for i in range(1,len(self.csr.indptr)):
            for j in range(self.csr.indptr[i-1],self.csr.indptr[i]):
                ret+=str(i)+" "+str(self.csr.indices[j]+1)+" "+str(self.csr.data[j])+'\n'
        return ret

    def to_dense(self):
        return self.csr.todense()

class PICsr:
    def __init__(self , matrixs):
        if("float32"==str(matrixs.dtype)):
            self.type=1
        else:
            self.type=0
        self.rgba = np.zeros(len(matrixs),dtype=CSR)
        self.m = len(matrixs[0])
        self.n = len(matrixs[0][0])
        for i in range(len(matrixs)):
            self.rgba[i] = CSR(matrixs[i])

    def write_mtx(self, file_path,name_):
        name="RGB"
        for i in range(3):
            on = open(file_path+name[i]+"_"+name_+".mtx","w")
            on.write(self.rgba[i].tostr())
            on.close()
    def write_pic(self, file_path):
        mpx = np.zeros((self.m,self.n,len(self.rgba)))
        for i in range(3):
            mpx[::, 0:, i] = self.rgba[i].to_dense()
            print(self.rgba[i].csr.data.shape)
        if(len(self.rgba)==4):
            mpx[::, 0:, 3]=1
        if(self.type==1):
            mpx = mpx*255
        mpx = np.array(mpx,dtype='u1')
        mpx = mpx*1/255

        print(mpx.shape)
        mpimg.imsave(file_path,mpx)

def read_png(file,pic_file,mtx_file):
    picture = mpimg.imread(file)
    picture = np.array(picture)
    ze = np.zeros(( len(picture[0][1])),dtype=picture.dtype)
    picture = np.insert(picture,0,values=ze,axis=1)
    r = len(ze)
    mat = np.zeros((r,len(picture),len(picture[0])),dtype=picture.dtype)
    for i in range(r):
        mat[i] = picture[::, 0:, i]
    mat = np.diff(mat)
    s = PICsr(mat)

    name = os.path.basename(file)
    name = os.path.splitext(name)[0]
    s.write_mtx(mtx_file,name)
    s.write_pic(pic_file+name+".png")

if __name__ == '__main__':
    read_png(sys.argv[1],sys.argv[2],sys.argv[3])
