import numpy as np
import json
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
def distance(data):
    slice=0
    dis={}
    np.save("datatest.npy",data)
    for i in data[:,0:3]:
        slice+=1
        tdis=[]
        for j in data[slice:,0:3]:
            t=np.linalg.norm((i-j),ord=2)
            tdis.append(t)
        dis[str(slice-1)]=tdis
    # with open("datadistance.txt","w") as f:
    #     disstr=json.dumps(dis)
    #     f.write(disstr)
    return dis

def clustermin(dis,cnum):
    catagory={}
    hierachy=[]
    for i in range(len(dis.keys())+1):
        i=str(i)
        catagory[i]=[i]
    c=catagory.copy()
    minx=''
    miny=''
    # mindis=10000
    while len(catagory.keys())>4:
        tempMin = 10000
        for k in catagory.keys():
            for subk in catagory[k]:
                if subk==str(len(dis)):
                    continue
                subk=str(subk)
                if min(dis[subk])<tempMin:
                    minsub=subk
                    offset = dis[minsub].index(min(dis[subk]))
                    if str(int(subk)+1+offset) in catagory[k]:
                        pass
                    else:
                        tempMin = min(dis[subk])
                        minx = int(k)
                        miny = int(subk) + 1 + offset

        # if mindis>tempMin:
        if str(miny) in catagory:
            t_i=0
            for i in catagory.keys():
                if str(minx) in catagory[i]:
                    t_i=i
            print(catagory[t_i], 'plus',catagory[str(miny)])
            catagory[t_i]+=(catagory[str(miny)])
            del catagory[str(miny)]
            print('so we get',catagory[t_i])
        else:
            t_i=0
            for i in catagory.keys():
                if str(miny) in catagory[i]:
                    t_i=i
            for j in catagory.keys():
                if str(minx) in catagory[j]:
                    print(catagory[t_i],'plus',catagory[j])
                    catagory[t_i]+=catagory[j]
                    del catagory[j]
                    print('and we get',catagory[t_i])
                    break
        # print("now still",len(catagory.keys()),"classes left")
    return  catagory


def calmax(distance,c1,c2):

    maxdis = 0
    for i in c1:
        for j in c2:
            if distance[int(i)][int(j)] > maxdis:
                maxdis = distance[int(i)][int(j)]
    return maxdis

def clustermax(dis,cnum):
    catagory = {}
    hierachy = []
    distance = np.zeros((2000, 2000))
    for i in range(1999):
        distance[i, i + 1:] = np.array(dis[str(i)])
        distance[i][i] = -100000
    distance[1999][1999] = -100000
    distance = distance + distance.T

    # distance = np.zeros((2000, 2000))
    # for i in range(1999):
    #     distance[i, i + 1:] = np.array(dis[str(i)])
    #     distance[i][i] = 100000
    # distance[1999][1999] = 100000
    # distance = distance + distance.T

    for i in range(len(dis.keys()) + 1):
        i = str(i)
        catagory[i] = [i]
    c = catagory.copy()
    minx = ''
    miny = ''
    # mindis=10000
    while len(catagory.keys()) > 4:
        print(len(catagory.keys()))
        tempmax = 0
        maxlist=[]
        xylist=[]

        for k in catagory.keys():
            kmax=0
            for subk in catagory.keys():
                if subk == k:
                    continue
                maxdis=calmax(distance,catagory[k],catagory[subk]) # maxdis 是k对于subk的最大距离
                if maxdis>kmax:
                    kmax=maxdis
                    kx=k
                    ky=subk
            maxlist.append(kmax)
            xylist.append([kx,ky])
        index=maxlist.index(min(maxlist))
        minx=xylist[index][0]
        miny=xylist[index][1]
        # if mindis>tempMin:
        if str(miny) in catagory:
            t_i = 0
            for i in catagory.keys():
                if str(minx) in catagory[i]:
                    t_i = i
            print(catagory[t_i])
            print('plus')
            print(catagory[str(miny)])
            catagory[t_i] += (catagory[str(miny)])
            del catagory[str(miny)]
            print('so we get', catagory[t_i])
        else:
            t_i = 0
            for i in catagory.keys():
                if str(miny) in catagory[i]:
                    t_i = i
            for j in catagory.keys():
                if str(minx) in catagory[j]:
                    print(catagory[t_i])
                    print('plus')
                    print(catagory[j])
                    catagory[t_i] += catagory[j]
                    del catagory[j]
                    print('and we get', catagory[t_i])
                    break
        # print("now still",len(catagory.keys()),"classes left")
    return catagory

def caldis_ave(distance,c1,c2):
    dis=0
    for i in c1:
        for j in c2:
            dis+=distance[int(i)][int(j)]
    return dis/(len(c1)*len(c2))


def clusterave(dis,cnum):
    distance=np.zeros((2000,2000))
    for i in range(1999):
        distance[i,i+1:]=np.array(dis[str(i)])
        distance[i][i]=100000
    distance[1999][1999]=100000
    distance=distance+distance.T
    catagory={}
    for i in range(len(dis.keys())+1):
        i=str(i)
        catagory[i]=[i]
    c=catagory.copy()
    minx=''
    miny=''
    # mindis=10000
    while len(catagory.keys())>4:
        print(len(catagory.keys()))
        temp = 100000
        for k in catagory.keys():
            for subk in catagory.keys():
                t=caldis_ave(distance,[k],[subk])
                if t<temp:
                    temp=t
                    minx=k
                    miny=subk

        # if mindis>tempmin:
        if str(miny) in catagory:
            t_i=0
            for i in catagory.keys():
                if str(minx) in catagory[i]:
                    t_i=i
                    break

            print(catagory[t_i] )
            print("plus")
            print(catagory[str(miny)])
            catagory[t_i]+=(catagory[str(miny)])
            del catagory[str(miny)]
            print('so we get',catagory[t_i],"distance is",temp)
        else:
            t_i=0
            for i in catagory.keys():
                if str(miny) in catagory[i]:
                    t_i=i
            for j in catagory.keys():
                if str(minx) in catagory[j]:
                    print(catagory[t_i])
                    print("plus")
                    print(catagory[j])
                    catagory[t_i]+=catagory[j]
                    print('so we get', catagory[t_i], "distance is", temp)
                    del catagory[j]
                    break
        # print("now still",len(catagory.keys()),"classes left")
    return  catagory


if __name__=="__main__":
    # data1=np.random.randint(-20,0,(500,3))
    # data2=np.random.randint(20,23,(500,3))
    # data3=np.random.randint(25,45,(500,3))
    # data4=np.random.randint(-100,-40,(500,3))
    # data=np.concatenate((data1,data2),axis=0)
    # data=np.concatenate((data,data3),axis=0)
    # data = np.concatenate((data, data4), axis=0)
    # lable=np.arange(0,2000,1).reshape(2000,1)
    # data=np.concatenate((data,lable),axis=1) # concat horizontally


    #test
    # data1 = np.random.randint(-20, 0, (20, 3))
    # data2 = np.random.randint(20, 23, (20, 3))
    # data3 = np.random.randint(10, 20, (40, 3))
    # data4 = np.random.randint(-30, -10, (40, 3))
    # data=np.concatenate((data4,data3),axis=0)
    # lable = np.arange(0, 80, 1).reshape(80, 1)
    # data = np.concatenate((data, lable), axis=1)  # concat horizontally

    # 读入存储的数据集
    data=np.load("data.npy")

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(data[0:500,0],data[0:500,1],data[0:500,2],color='r')
    # ax.scatter(data[500:1000,0],data[500:1000,1],data[500:1000,2],color='y')
    # ax.scatter(data[1000:1500, 0], data[1000:1500, 1], data[1000:1500, 2], color='b')
    # ax.scatter(data[1500:2000, 0], data[1500:2000, 1], data[1500:2000, 2], color='g')
    # plt.show()
    # dis=distance(data)
    # del dis['79']

    # 读入存储的距离
    with open("datadistance.txt","r") as f:
        dis=f.read()
        dis=json.loads(dis)
        del dis['1999']

    #在这里切换不同的算法
    # catagory=clustermin(dis,5)  # 单链接
    # catagory=clustermax(dis,5)    # 全连接
     catagory=clusterave(dis,5)  # 平均距离


    catastr=json.dumps(catagory)
    with open('clu1.txt','w') as f:
        f.write(catastr)
    # with open('clu2.txt','r')as f:
    #     catagory=f.read()
    #     catagory=json.loads(catagory)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color=('r', 'b', 'g', 'y', 'o')
    ci=0
    for i in catagory.keys():
        c=color[ci]
        print(catagory[i])
        x=[]
        y=[]
        z=[]
        for j in catagory[i]:
            item=int(j)
            x.append(data[item][0])
            y.append(data[item][1])
            z.append(data[item][2])
        ax.scatter(x,y, z, color=c)
        ci+=1
    plt.show()



