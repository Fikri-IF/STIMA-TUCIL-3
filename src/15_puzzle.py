import numpy as np
from copy import deepcopy
import time
import sys

def is_have_solution(arr_for_checking,black_tile):
    que=[0 for i in range (16)]
    sum=0
    for i in range(np.size(arr_for_checking)):
        #component=0
        if arr_for_checking[i]==16 and i in black_tile:
            sum+=1
        for j in range(i+1,np.size(arr_for_checking)):
            if arr_for_checking[i]>arr_for_checking[j]:
                sum+=1
                que[arr_for_checking[i]-1]+=1
    for i in range(16):
        print("Nilai fungsi Kurang("+str(i+1)+") = " + str(que[i]))
    print("\nTotal nilai Fungsi KURANG(i) + X adalah " + str(sum)+"\n")
    if sum%2==0:
        return True
    else:
        return False

def display_matrix(matrix):
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 16:
                print(" \t",end="")
            else:
                print(str(matrix[i][j])+"\t",end="")
        print("")

def move_right(state,x,y):
    temp = state[x][y]
    state[x][y]=state[x][y+1]
    state[x][y+1]=temp
    return state
    
def move_up(state,x,y):
    temp = state[x][y]
    state[x][y]=state[x-1][y]
    state[x-1][y]=temp
    return state

def move_left(state,x,y):
    temp = state[x][y]
    state[x][y]=state[x][y-1]
    state[x][y-1]=temp
    return state

def move_down(state,x,y):
    temp = state[x][y]
    state[x][y]=state[x+1][y]
    state[x+1][y]=temp
    return state

def get_blank_location(arr):
    for i in range(4):
        for j in range(4):
            if arr[i][j]==16:
                x=i
                y=j
                break
    return x,y

def count_cost(arr):
    cost=0
    arr_for_checking=np.ravel(arr)
    for i in range(np.size(arr_for_checking)):
        if arr_for_checking[i] != 16 and i+1!=arr_for_checking[i]:
            cost+=1
    return cost

def get_cost(node_):
    return node_.cost,node_.depth

def ins_to_que(que_,node_):
    que_.append(node_)
    que_.sort(key=get_cost) #Mengurutkan simpul hidup berdasarkan cost lalu jika sama, berdasarkan kedalaman simpul

def move(que_,moved,node_):
    x,y=get_blank_location(moved)
    moved_node = node(moved,node_,node_.depth+1,x,y,count_cost(moved)+node_.depth+1)
    ins_to_que(que_,moved_node)

def visited_or_not(visited,moved):
    i=0
    ada=False
    while(i<len(visited) and ada==False):
        if np.array_equal(visited[i],moved):
            ada=True
        i+=1
    return ada

def solve(sol_,que_,node_,visited):
    next_node=node_
    global node_generated
    while not(np.array_equal(goal_state,next_node.state)): #Hingga menemukan hasil akhir
        if next_node.x != 0:
            moved = move_up(deepcopy(next_node.state),next_node.x,next_node.y)
            if not(visited_or_not(visited,moved)): #Jika susunan puzzle belum pernah dijumpai maka, dimasukkan ke dalam simpul hidup
                move(que_,moved,next_node)
                node_generated+=1
                visited.append(moved) #Me-list semua susunan puzzle yang pernah dijumpai
        if next_node.y != 3:
            moved = move_right(deepcopy(next_node.state),next_node.x,next_node.y)
            if not(visited_or_not(visited,moved)):
                move(que_,moved,next_node)
                node_generated+=1
                visited.append(moved)
        if next_node.x != 3:
            moved = move_down(deepcopy(next_node.state),next_node.x,next_node.y)
            if not(visited_or_not(visited,moved)): 
                move(que_,moved,next_node)
                node_generated+=1
                visited.append(moved)
        if next_node.y !=0:
            moved = move_left(deepcopy(next_node.state),next_node.x,next_node.y)
            if not(visited_or_not(visited,moved)):
                move(que_,moved,next_node)
                node_generated+=1
                visited.append(moved)
        next_node=que_.pop(0) #Mengambil node dengan cost terkecil
    sol_.append(next_node) 
    que_.clear() #Menghapus semua antrian simpul hidup

def display_path(node_):
    if node_.parents_node != None:
        display_path(node_.parents_node)
        display_matrix(node_.state)
        print("\n")
    else:
        display_matrix(node_.state)
        print("\n")

def teks_to_matriks(_inputfile):
    _case = []
    with open(_inputfile) as file:
        for item in file:
            _case.append([int(i) for i in item.split()])
    return _case

class node(object):
    def __init__(self,state,parents_node,depth,Xblank_location,Yblank_location,cost):
        self.state=state
        self.parents_node=parents_node
        self.depth=depth
        self.x=Xblank_location
        self.y=Yblank_location
        self.cost=cost

if __name__ == '__main__':
    print("\n\n=== Penyelesaian Persoalan 15-Puzzle dengan Algoritma Branch and Bound ===\n")
    goal_state=np.array([
        [1,2,3,4],
        [5,6,7,8],
        [9,10,11,12],
        [13,14,15,16]
    ])
    input_file= input("\nMasukkan file .txt yang akan digunakan sebagai test case : ")
    is_= teks_to_matriks("test/"+input_file)

    black_tile=[1,3,4,6,9,11,12,14]
    arr_for_checking=np.ravel(is_) #Mengubah matriks mencjadi 1 dimensi untuk pengecekan fungsi KURANG(i)
    node_generated = 0 #Total jumlah simpul yang terbentuk

    print("Puzzle Awal  : \n")
    display_matrix(is_)
    print("")

    if is_have_solution(arr_for_checking,black_tile):
        back_to_2d = arr_for_checking.reshape(4,4) #mengembalikan bentuk menjadi 2d

        #initiate root ---------------------------
        urutan=[] #List simpul hidup
        sol=[] #Jawaban
        visited=[] #List simpul yang pernah dikunjungi
        x_start,y_start=get_blank_location(back_to_2d)
        start_node = node(back_to_2d,None,0,x_start,y_start,99)
        urutan.append(start_node)
        #initiate root ---------------------------

        #Runtime-----------------------
        start_time = time.time()
        solve(sol,urutan,start_node,visited)
        selesai=time.time()-start_time
        #Runtime-----------------------

        print("\nLangkah Penyelesaian\n")
        display_path(sol[0])
        print("Jumlah simpul yang dibangkitkan = "+str(node_generated)+"\n")
        print("Total waktu eksekusi penyelesaian : " + str(selesai))
        

    else:
        print("\nGA BISA DISELESAIIN NICH")