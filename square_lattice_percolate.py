import numpy as np
import random
import pylab

##L=128
L=64
N=L**2
empty=-(N+1)

ptr=np.zeros(N, dtype=int)               # array of pointers
nn=np.zeros((N, 4), dtype=int)           # nearest neighbors
order=np.zeros(N, dtype=int)             # occupation number


# Setting the boundaries
def boundaries():
        for i in range(N):
                nn[i, 0]=(i+1)%N
                nn[i, 1]=(i+N-1)%N
                nn[i, 2]=(i+L)%N
                nn[i, 3]=(i+N-L)%N

                if i%L==0: nn[i, 1]=i+L-1
                if (i+1)%L==0: nn[i, 0]=i-L+1

# Generating the random orders of site occupation
def permutation():
        j=0
        temp=0
        for i in range(N):
                order[i]=i
                for i in range(N):
                        j=i+(N-i)*random.random()
                        temp=np.copy(order[i])
                        order[i]=order[j]
                        order[j]=temp

# Find operation
def findroot(i):
        r=s=i
        while ptr[r]>0:
                ptr[s]=np.copy(ptr[r])
                s=r
                r=ptr[r]
        return r

# main algorithm
def percolate():
        X=[]
        Y=[]
        big=0
        for i in range(N): ptr[i]=empty

        for i in range(N):
                r1=s1=np.copy(order[i])
                ptr[s1]=-1
                
                for j in range(4):
                        s2=np.copy(nn[s1, j])
                        if ptr[s2] != empty:
                                r2=findroot(s2)
                                if (r2!=r1):
                                        if ptr[r1]>ptr[r2]:
                                                ptr[r2]=ptr[r2]+ptr[r1]
                                                ptr[r1]=r2
                                                r1=np.copy(r2)
                                        else:
                                                ptr[r1]=ptr[r1]+ptr[r2]
                                                ptr[r2]=r1
                                        if -ptr[r1]>big: big=-np.copy(ptr[r1])

##                print i+1," ", big
                X+=[(i+1.)/N, ]
                Y+=[big, ]
        pylab.plot(X, Y, '-')
        pylab.xlabel("Percolation Probability")
        pylab.ylabel("Size of the largest cluster")
        pylab.title("N = 64 X 64")
        pylab.show()

boundaries()
permutation()
percolate()