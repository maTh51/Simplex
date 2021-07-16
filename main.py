import sys
import numpy as np

def get_vo(v):
    count = 0
    for e in v:
        count = count + e
    return count

def pl_otima(ct, A, n):
    print("otima")
    print(get_vo(ct))
    for i in range(n-1):
        print(A[i,i], end=" ")
    print(A[-1,-1])
    for i in range(len(ct) - 1):
        print(ct[i],end=" ")
    print(ct[-1])


def tableaux(ct,A,b,n,m):
    c = np.array([-x for x in ct])

    T = np.block([
        [np.zeros(n), c, np.zeros(n), 0],
        [np.eye(n), A, np.eye(n), b]
    ])
    
    print(T)



if __name__ == "__main__":

    # Lendo entrada
    entrada = sys.stdin.read()
    entrada = entrada.split()

    n = int(entrada[0])
    m = int(entrada[1])
    ct = np.array([int(x) for x in entrada[2:(2+m)]])

    aux = []
    for i in range(n):
        aux.append([int(x) for x in entrada[(2+m+i*(m+1)):(2+m+i*(m+1)+m+1)]])

    Ab = np.matrix(aux)

    A = np.matrix(Ab[:,:m])
    b = np.array(Ab[:,-1])

    tableaux(ct,A,b,n,m)
    # Primeiro caso: tableaux já no estado ótimo
    # if(n == m):
    #     if((A == np.eye(n)).all() and (ct >= 0).all()):
    #         pl_otima(ct, A, n)
    #         exit(0)
    #     else:
    #         print("Nop")

