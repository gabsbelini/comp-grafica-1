# -*- coding: utf-8 -*-
#import numpy as np
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.rcParams['backend'] = "qt4agg"
plt.rcParams['backend.qt4'] = "PySide"
#import linecache
from tkinter import *


__author__ = 'gabss'
def Principal(arq1, arq2,plotar):

    '''CONFIGURAÇÃO DOS ARQUIVOS .TXT:
    objeto.txt: 1°linha: numero de vértices do objeto (NV).
                "NV" linhas seguintes: Coordenadas (x,y,z) dos vértices do objeto.
                Próxima linhas após os vértices: Número de superfícies (NS).
                Restante das linhas: Número de vértices por superfície para cada superfície (NS)
    vps: Cada linha contém uma sequência de vértices enumerados de 1 até NV (cada número representa um vértice baseado na posição
     das coordenadas dos vértices no arquivo objeto.txt).
    pontos.txt: Contém as coordenadas dos pontos P1, P2, P3, uma em cada linha, respectivamente, são fornecidos pelo usu
    ário em tempo de execução.
    pontodevista.txt: Contém as coordenadas do ponto de vista C = (a,b,c), são fornecidos pelo usuário em tempo de execu-
    ção.
    '''

    def recebePontoDeVista(): # recebe ponto de vista C=(a,b,c)
        arquivo = open('pontodevista.txt', 'r')
        pontodevista = [float(x) for x in arquivo.readline().split()]
        return pontodevista

    def recebePonto(): # recebe coordenadas dos pontos P1,P2,P3
        arquivo = open('pontos.txt', 'r')
        P1 = [float(x) for x in arquivo.readline().split()]
        P2 = [float(x) for x in arquivo.readline().split()]
        P3 = [float(x) for x in arquivo.readline().split()]
        return P1, P2, P3

    def criaMatrizObjeto(NV,lista_de_coordenadas, arq1):# cria matriz do objeto de ordem 4xNV, em coordenadas homogêneas
        k = 1
        x = 0
        arquivo = open(arq1+'.txt', 'r')
        arquivo.readline()
        lista_de_coordenadas = np.array(lista_de_coordenadas)
        lista_de_coordenadas = lista_de_coordenadas.transpose()
        newrow = []
        while x < NV:
            newrow.append(k)
            x += 1
        Mobj = np.vstack([lista_de_coordenadas, newrow])
        print(Mobj)
        arquivo.close()
        return Mobj

    '''recebeObjeto() tem a função de ler o número de vértices NV, todas as corrdenadas dos "NV" vértices e também o número
    de superfícies (NS), todos esses dados devem ser inseridos no arquivo objeto.txt.
    As coordenadas dos vértices são armazenadas em uma lista de tuplas no tipo "lista = [(x0,y0,z0), (x1,y1,z1), ...]"
    '''
    def recebeObjeto(arq1):
        lista_de_coordenadas = []
        arquivo = open(arq1+'.txt', 'r')
        NV = int(arquivo.readline())
        for x in range(0, NV):
            lista = []
            lista = [float(x) for x in arquivo.readline().split()]
            lista = tuple(lista)
            lista_de_coordenadas.append(lista)
        NS = int(arquivo.readline())
        print(NV,'\n', lista_de_coordenadas,'\n', NS)
        arquivo.close()
        return NV, lista_de_coordenadas, NS

    #Cria listas pltx, plty, pltz com as coordenadas necessárias para plotar cada superfície, uma de cada vez.
    def definePlotCoords3D(S, Mobj,dx, lista_x, lista_y, lista_z):
        plt_x = []
        plt_y = []
        plt_z = []
        for k in S:
            x = Mobj[0][k-1] #recebe a coordenada x da matriz do objeto
            y = Mobj[1][k-1]
            z = Mobj[2][k-1]
            plt_x.append(x)#Recebe todas as coordenadas x para plotar a superfície S
            plt_y.append(y)
            plt_z.append(z)
        dx.scatter(lista_x, lista_y, lista_z) #Plota os pontos no plano 3D
        dx.plot(plt_x, plt_y, plt_z)#Plota as linhas no plano 3D

    #Lê a ordem e o número dos vértices no arquivo vps.txt e chama a função definePlotCoords3D para plotar as superfícies
    def plota3D(NS, Mobj, lista_x, lista_y, lista_z, arq2):
        fig = plt.figure()
        dx = fig.add_subplot(111, projection='3d')
        dx.set_title('3D Plot')
        arquivo = open(arq2+'.txt','r')
        for x in range(0,NS):
            S = [int(x) for x in arquivo.readline().split()]
            definePlotCoords3D(S, Mobj,dx, lista_x, lista_y, lista_z)


    #Idem definePlotCoords3D, mas para 2D agora.
    def definePlotCoords(V, PlinhaPlano, PlinhaParPlano,cx,ax,cont):
        plt_x = []
        plt_y = []
        pltpar_x = []
        pltpar_y = []
        for k in V:
            x = PlinhaPlano[0][k-1]
            y = PlinhaPlano[1][k-1]
            xpar = PlinhaParPlano[0][k-1]
            ypar = PlinhaParPlano[1][k-1]
            pltpar_x.append(xpar)
            pltpar_y.append(ypar)
            plt_x.append(x)
            plt_y.append(y)
        if cont == 2:
            ax.plot(plt_x, plt_y)
            cx.plot(pltpar_x, pltpar_y)
        elif cont == 0:
            ax.plot(plt_x, plt_y)
        elif cont == 1:
            cx.plot(pltpar_x, pltpar_y)
    #Idem plota3D, mas para 2D agora.
    def plota2D(NS, PlinhaPlano,arq2, PlinhaParPlano, cont):
        ax = 41
        cx = 39
        if cont == 2:
            figx = plt.figure()
            ax = figx.add_subplot(111)
            ax.set_title('Projeção Cônica')
            figs = plt.figure()
            cx = figs.add_subplot(111)
            cx.set_title('Projeção Paralela')
        elif cont == 0:
            figx = plt.figure()
            ax = figx.add_subplot(111)
            ax.set_title('Projeção Cônica')
        elif cont == 1:
            figs = plt.figure()
            cx = figs.add_subplot(111)
            cx.set_title('Projeção Paralela')
        arquivo = open(arq2+'.txt','r')
        for x in range(0,NS):
            V = [int(x) for x in arquivo.readline().split()]
            definePlotCoords(V, PlinhaPlano,PlinhaParPlano,cx,ax,cont)

    # faz produto vetorial entre 2 vetores contidos no plano e retorna o vetornormal ao plano em 'prodvetorial'
    def encontraVetornormal(P1P2, P2P3):
        prodvetorial = np.cross(P1P2, P2P3)
        print('Produto Vetorial',prodvetorial)
        return prodvetorial

    def encontraVetor(P1, P2): # encontra um vetor "P2 - P1" contido no plano.
        Vetor = []
        print('ponto1',P1)
        print('ponto2',P2)
        for x in range (0, 3):
            Vetor.append(P2[x] - P1[x])
        print('Vetor P2-P1',Vetor)
        return Vetor

    #calcula "d0 = x0.nx + y0.ny + z0.nz" e "d1 = a.nx + b.ny + c.nz"
    def calculad0_d1(P1, prodvetorial):
        d0 = P1[0]*prodvetorial[0] + P1[1]*prodvetorial[1] + P1[2]*prodvetorial[2]
        return d0


    def criaMatrizPerspectivaPar(d,d0,prodvetorial, pontodevista):
        a = pontodevista[0]
        b = pontodevista[1]
        c = pontodevista[2]
        nx = prodvetorial[0]
        ny = prodvetorial[1]
        nz = prodvetorial[2]
        MperPar = [
            [(d+a*nx), -a*ny, -a*nz, (a)*d0],
            [-b*nx, (d-(b*ny)), -b*nz, b*d0],
            [-c*nx, -c*ny, d-(c*nz), c*d0],
            [0, 0, 0, d1],
                 ]
        MperPar = np.array(MperPar)
        return MperPar

    # monta a Mper com seus valores para posterior multiplicação.
    def criaMatrizPerspectiva(d, d0, prodvetorial, pontodevista):
        a = pontodevista[0]
        b = pontodevista[1]
        c = pontodevista[2]
        nx = prodvetorial[0]
        ny = prodvetorial[1]
        nz = prodvetorial[2]
        Mper = [
            [(d+a*nx), a*ny, a*nz, (-a)*d0],
            [b*nx, (d+(b*ny)), b*nz, -b*d0],
            [c*nx, c*ny, d+(c*nz), -c*d0],
            [nx, ny, nz, -d1],
                 ]
        Mper = np.array(Mper)
        print('Matriz Perspectiva,', Mper)
        return Mper

    # encontra P' = Mper.P
    def multiplicaMatrizPerspectivaPonto(Mper, Mobj, MperPar):
        Plinha = np.dot(Mper, Mobj)
        PlinhaPar = np.dot(MperPar, Mobj)
        print('Homogenea', Plinha)
        return Plinha, PlinhaPar

    # transforma P' em coordenadas cartesianas
    def transformaCartesiana(Plinha, PlinhaPar):
        i=0
        j=0
        PlinhaPar = np.array(PlinhaPar)
        Plinha = np.array(Plinha)
        for i in range(3):
            for j in range(0, NV):
                Plinha.itemset((i,j), (Plinha.item(i,j)/Plinha.item(3,j)))
        i=0
        j=0
        for i in range(3):
            for j in range(0, NV):
                PlinhaPar.itemset((i,j), (PlinhaPar.item(i,j)/PlinhaPar.item(3,j)))
        print("P'",Plinha)
        PlinhaParCartesiana = PlinhaPar
        PlinhaCartesiana = Plinha
        print('Coordenadas Cartesianas \n', PlinhaCartesiana)
        return PlinhaCartesiana, PlinhaParCartesiana

    # Transforma coordenadas cartesianas para coordenadas do plano
    def transformaPlano(PlinhaCartesiana, PlinhaParCartesiana):
        PlinhaParPlano = np.delete(PlinhaParCartesiana, (3,2),0)
        PlinhaPlano = np.delete(PlinhaCartesiana, (3,2),0)
        print('Coordenadas do Plano: \n', PlinhaPlano)
        return PlinhaPlano, PlinhaParPlano


    # cria listas com todas coordenadas de cada eixo, serão usadas para plotar os vértices em 3D
    def modificaParaPlotar3D(lista_de_coordenadas):
        lista_x = []
        lista_y = []
        lista_z = []
        for x,y,z in lista_de_coordenadas:
            lista_x.append(x)
            lista_y.append(y)
            lista_z.append(z)
        return lista_x, lista_y, lista_z

    #fig = plt.figure()
    #ax = plt.subplot(111)
    pontodevista = recebePontoDeVista() # C = (a,b,c)
    P1, P2, P3 = recebePonto()
    NV, lista_de_coordenadas, NS = recebeObjeto(arq1)
    Mobj = criaMatrizObjeto(NV, lista_de_coordenadas, arq1)
    Vetor_1 = encontraVetor(P1, P2) # Faz P2-P1 pra achar um vetor paralelo ao plano
    Vetor_2 = encontraVetor(P3, P2) #Faz P2-P3 pra achar outro vetor paralelo ao plano
    prodvetorial = encontraVetornormal(Vetor_1, Vetor_2)
    d0 = calculad0_d1(P1, prodvetorial)
    d1 = calculad0_d1(pontodevista, prodvetorial)
    d = d0 - d1
    Mper = criaMatrizPerspectiva(d, d0, prodvetorial, pontodevista)
    MperPar = criaMatrizPerspectivaPar(d, d0, prodvetorial, pontodevista)
    Plinha, PlinhaPar = multiplicaMatrizPerspectivaPonto(Mper, Mobj, MperPar) # P' = Mper.P
    PlinhaCartesiana, PlinhaParCartesiana = transformaCartesiana(Plinha, PlinhaPar)
    PlinhaPlano, PlinhaParPlano = transformaPlano(PlinhaCartesiana, PlinhaParCartesiana)
    lista_x, lista_y, lista_z = modificaParaPlotar3D(lista_de_coordenadas)
    #esse 'if' serve para tratar as checkbox da interface, a checkbox plota3D retorna valor 3 quando marcada e a
    #checkbox plota2D retorna valor 5 quando marcada, ambas quando nao marcadas tem valor 0, plotar = plotar2d+plotar3d.
    if plotar == 15:#as 3
        cont = 2
        plota2D(NS, PlinhaPlano, arq2, PlinhaParPlano, cont)
        plota3D(NS, Mobj, lista_x, lista_y, lista_z, arq2)
    elif plotar == 10:# conica + 3d
        cont = 0
        plota2D(NS, PlinhaPlano, arq2,PlinhaParPlano,cont)
        plota3D(NS, Mobj, lista_x, lista_y, lista_z, arq2)
    elif plotar == 12:# conica+paralela
        cont = 2
        plota2D(NS, PlinhaPlano, arq2,PlinhaParPlano,cont)
    elif plotar == 8: #paralela + 3d
        cont = 1
        plota2D(NS, PlinhaPlano, arq2,PlinhaParPlano,cont)
        plota3D(NS, Mobj, lista_x, lista_y, lista_z, arq2)
    elif plotar == 7:# conica
        cont = 0
        plota2D(NS, PlinhaPlano, arq2,PlinhaParPlano,cont)
    elif plotar == 5:# paralela
        cont = 1
        plota2D(NS, PlinhaPlano, arq2,PlinhaParPlano,cont)
    elif plotar == 3:# 3d
        plota3D(NS, Mobj, lista_x, lista_y, lista_z, arq2)
    else:
        print('selecione uma projecao a ser plotada')

    plt.show() # Mostra o que foi plotado


#recebimento de valores através da interface, posicionamento de botoes, inputtexts, etc...
root = Tk()



def recebeDataIHC(event):
    P1 = []
    P2 = []
    P3 = []
    a = entry1.get()
    b = entry2.get()
    c = entry3.get()
    P1.append(entry4.get())
    P1.append(entry5.get())
    P1.append(entry6.get())
    P2.append(entry7.get())
    P2.append(entry8.get())
    P2.append(entry9.get())
    P3.append(entry10.get())
    P3.append(entry11.get())
    P3.append(entry12.get())
    arq1 = entry13.get()
    arq2 = entry14.get()
    escreveArquivos(a, b, c, P1, P2, P3)
    plotar = plotar3d.get() + plotar2dpar.get() + plotar2dcon.get()
    Principal(arq1, arq2, plotar)

def escreveArquivos(a, b, c, P1, P2, P3):
    C = open('pontodevista.txt', 'w')
    C.write(a + ' ' + b + ' ' + c)
    Pontos = open('pontos.txt', 'w')
    Pontos.write(P1[0]+ ' '+ P1[1]+ ' '+ P1[2])
    Pontos.write('\n')
    Pontos.write(P2[0]+ ' '+ P2[1]+ ' '+ P2[2])
    Pontos.write('\n')
    Pontos.write(P3[0]+ ' '+ P3[1]+ ' '+ P3[2])
    C.close()
    Pontos.close()

botao = Label(root, text='Plotar', bg='green', fg='white',width=20, height=2)
botao.grid(row=11, column=1,columnspan=2)


plotar3d = IntVar()
plotar2dpar = IntVar()
plotar2dcon = IntVar()
c1 = Checkbutton(root, text="Plotar objeto 3D", variable=plotar3d, onvalue=3, offvalue=0)
c2 = Checkbutton(root, text="Plotar Projeção Paralela", variable=plotar2dpar, onvalue=5, offvalue=0)
c3 = Checkbutton(root, text="Plotar Projeção Cônica", variable=plotar2dcon, onvalue=7, offvalue=0)

botao.bind('<Button-1>', recebeDataIHC)
frame = Frame(root, width=1000, height=1000)
label1_pontodevista = Label(root, text='Ponto de Vista')
label2_a = Label(root, text='a')
label3_b = Label(root, text='b')
label4_c = Label(root, text='c')
label5_Pontos = Label(root, text='Pontos')
label6_P1 = Label(root, text='P1')
label7_P2 = Label(root, text='P2')
label8_P3 = Label(root, text='P3')
label9_X = Label(root, text='X')
label10_Y = Label(root, text='Y')
label11_Z = Label(root, text='Z')
label12_objeto = Label(root, text='Arquivo Objeto:')
label13_vps = Label(root, text='Arquivo VPS:')
entry1 = Entry(root, width=3)
entry2 = Entry(root,width=3)
entry3 = Entry(root,width=3)
entry4 = Entry(root,width=3)
entry5 = Entry(root,width=3)
entry6 = Entry(root,width=3)
entry7 = Entry(root,width=3)
entry8 = Entry(root,width=3)
entry9 = Entry(root,width=3)
entry10 = Entry(root,width=3)
entry11 = Entry(root,width=3)
entry12 = Entry(root,width=3)
entry13 = Entry(root,width=11)
entry14 = Entry(root,width=11)

label1_pontodevista.grid(row=0, column=0, sticky=W,padx=10)
label2_a.grid(row=1, column=0,sticky=W,padx=10)
label3_b.grid(row=2, column=0,sticky=W,padx=10)
label4_c.grid(row=3, column=0,sticky=W,padx=10)
label5_Pontos.grid(row=4, column=0, sticky=W,padx=46)
label6_P1.grid(row=6, column=0,sticky=W,padx=10)
label7_P2.grid(row=7, column=0,sticky=W,padx=10)
label8_P3.grid(row=8, column=0,sticky=W,padx=10)
label9_X.grid(row=5, column=0,sticky=W,padx=35)
label10_Y.grid(row=5, column=0,sticky=W,padx=63)
label11_Z.grid(row=5, column=0,sticky=W,padx=91)
label12_objeto.grid(row=0, column=2,sticky=E)
label13_vps.grid(row=1, column=2, sticky=E)

entry1.grid(row=1, column=0, sticky=W,padx=30)
entry2.grid(row=2, column=0, sticky=W,padx=30)
entry3.grid(row=3, column=0,sticky=W,padx=30)
entry4.grid(row=6, column=0,sticky=W,padx=30)
entry5.grid(row=6,column=0, sticky=W,padx=58)
entry6.grid(row=6, column=0, sticky=W,padx=86)
entry7.grid(row=7, column=0,sticky=W,padx=30)
entry8.grid(row=7, column=0,sticky=W,padx=58)
entry9.grid(row=7, column=0, sticky=W,padx=86)
entry10.grid(row=8, column=0,sticky=W,padx=30)
entry11.grid(row=8, column=0,sticky=W,padx=58)
entry12.grid(row=8, column=0, sticky=W,padx=86)
entry13.grid(row=0, column=3)
entry14.grid(row=1, column=3)
c1.grid(row=10, column=0,sticky=W)
c2.grid(row=11, column=0,sticky=W)
c3.grid(row=12, column=0,sticky=W)
root.mainloop() #Loop da interface