import sys
import numpy as np

def build_tableaux(ct,A,b,n,m):
    c = np.array([-x for x in ct])

    T = np.block([
        [np.zeros(n), c, np.zeros(n), 0],
        [np.eye(n), A, np.eye(n), b]
    ])

    return T

def build_tableaux_aux(A,b,n,m,v):
    c = np.block([np.zeros(m+n),np.ones(n)])

    I_aux = np.eye(n)
    I2_aux = np.eye(n)
    for e in v:
        I_aux[e,e] = I_aux[e,e]*(-1)
        I2_aux[e,e] = I2_aux[e,e]*(-1)

    T = np.block([
        [np.zeros(n), c, 0],
        [I2_aux, A, I_aux, np.eye(n), b]
    ])

    for i in range(1,n+1):
        T[0,:] += (-1)*T[i,:]

    return T

def get_base(T,n,m):
    for i in range(n,n+m+1):
        if(T[0,i] != 0 and np.array_equal(T[1:,i], T[1:,i].astype(bool))):
            # print(T[1:,i])
            for j in range(1,n+1):
                if(T[j,i] == 1):
                    T[0,:] = T[0,:]-((T[0,i])*T[j,:])
    return T



def set_forma_canonica(ct,A,b,n,m):
    if((b < 0).any()):
        faltam = []
        for i in range(len(b)):
            if(b[i] < 0):
                b[i] = b[i] * (-1)
                A[i,:] = A[i,:] * (-1)
                faltam.append(i)
        
        base, T = solve_pl_auxiliar(A,b,n,m,faltam)
        if(base == 0):
            T = np.block([T[:,0:2*n+m], T[:,-1]])
            c = np.array([-x for x in ct])
            T[0,n:n+m] = c
            # necessário limpar certificado Vero
            T[0,0:n] = np.zeros(n)

            T = get_base(T,n,m)
            solve_simplex(T,n,m)
        else:
            print_sol(T,2)


    else:
        T = build_tableaux(ct,A,b,n,m)
        solve_simplex(T,n,m)


def solve_pl_auxiliar(A,b,n,m,faltam):

    T_aux = build_tableaux_aux(A,b,n,m,faltam)
    return solve_simplex(T_aux,n,m, True)


def print_tableaux(T):
    for i in range((T.shape[1])):
        print(np.around(T[0,i], decimals=1)," ", " ",end="")
    print("")
    for i in range((T.shape[1])):
        print("_",end="")
    print("")
    for j in range(1,T.shape[0]):
        for i in range((T.shape[1])):
            print((np.around(T[j,i], decimals=1))," ", end="")
        print("")
    print("\n")
    
    
def solve_simplex(T,n,m, aux = False):
    
    flag_done = False
    while(not flag_done):
        # print_tableaux(T)
        if((T[0,n:2*n+m+1] >= 0).all()):
            flag_done = True
            if(not aux):
                print_sol(T,0)
                return
        else:
            for i in range(n, 2*n+m+1):
                if(T[0,i]) < 0:
                    pivo_col = i
                    break

            if((T[1:,pivo_col] <= 0).all()):
                flag_done = True
                if(not aux):
                    print_sol(T,1,pivo_col)
                    return
            else:
                razao = -1
                ind = 0
                for i in range(1, n+1):
                    if(T[i,pivo_col] > 0):
                        if(razao < 0 or razao > (T[i,-1]/T[i,pivo_col])):
                            razao = (T[i,-1]/T[i,pivo_col])
                            ind = i

                T[ind,:] = T[ind,:]/T[ind,pivo_col]
                for i in range(1,ind):
                    T[i,:] = T[i,:]-(T[i,pivo_col]*T[ind,:])
                for i in range(ind+1,n+1):
                    T[i,:] = T[i,:]-(T[i,pivo_col]*T[ind,:])
                T[0,:] = T[0,:]+(((-1)*T[0,pivo_col])*T[ind,:])
    if(aux):
        if(T[0,-1] < 0.0000001 and T[0,-1] > -0.0000001):
            T[0,-1] = 0
        if(T[0,-1] < 0):
            return(1, T)
        else:
            return(0, T)
    else:
        print_sol(T,2)
    

def print_sol(T,ans,pos = 0):
    if(ans == 0):
        print("otima")
        print(np.around(T[0,-1], decimals=7))
        for i in range(n,n+m):
            if(np.array_equal(T[1:,i], T[1:,i].astype(bool))):
                for j in range(1,n+1):
                    if T[j,i] == 1:
                        print(np.around(T[j,-1], decimals=7),end=" ")
            else:
                print("0.0",end=" ")
        print("")
        for i in range(0,n):
            print(np.around(T[0,i], decimals=7),end=" ")
        print("")
    
    elif(ans == 1):
        print("ilimitada")
        for i in range(n,n+m):
            if(np.array_equal(T[1:,i], T[1:,i].astype(bool))):
                for j in range(1,n+1):
                    if T[j,i] == 1:
                        print(np.around(T[j,-1], decimals=7),end=" ")
            else:
                print("0.0",end=" ")
        print("")
        for i in range(n,n+m):
            if(i == pos):
                print("1.0",end=" ")
            elif(np.array_equal(T[1:,i], T[1:,i].astype(bool))):
                for j in range(1,n+1):
                    if T[j,i] == 1:
                        print(np.around(T[j,pos]*(-1), decimals=7),end=" ")
            else:
                print("0.0",end=" ")       
        print("")
    
    else:
        print("inviavel")
        for i in range(0,n):
            print(np.around(T[0,i], decimals=7),end=" ")
        print("")
    
    exit(0)



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
    set_forma_canonica(ct,A,b,n,m)



