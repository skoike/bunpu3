# -*- coding: utf-8 -*-
#
#需給バランス
#
#
#
#
#需要は可処分所得×必要割合、可処分所得は所得×(1-負担率)、供給は人件費＋原価＋加工費
from bunpu import *
#
#需要を決めるパラメータ
#所得
income = Bunpu()
income.bunpu_hist('income.txt','income',0,1,[0,1],divn=[100], fs=36, volume=1)
#
#負担率の割合計算
futan=Bunpu()
#futan.bunpu_hist('futan_ratio_2022.txt','futan',0,1,[0,3],divn=[100], fs=36, volume=1)
futan.bunpu_hist('futan_ratio_1994.txt','futan',0,1,[0,3],divn=[100], volume=1)
vecone=Bunpu()
vecone.vector_gene([1])
kasyobunratio=vecone.bunpu_sub(futan)
kasyobunratio.bunpu_graph('kasyobunratio',fs=36)
#可処分所得
aftertax = income.bunpu_product(kasyobunratio,[100],[-1])
aftertax.bunpu_graph('aftertax', fs=36)
#嗜好割合、個人が可処分所得から支払ってもよいと考える割合
willpayratio = Bunpu()
willpayratio.bunpu_gene([0.01],[0.05],[0.02],[0.012],[100],gegg=[0,0], volume=6000)
willpayratio.bunpu_graph('willpayratio', shw=1, fs=36)
#需要分布
demand = Bunpu()

demand = aftertax.bunpu_product(willpayratio)
demand.bunpu_graph('demand',shw=1, fs=36)

#供給を決めるパラメータ
#商品化意欲比率、企業が生産リスクを負ってもよいと考える割合
willsellratio = Bunpu()
willsellratio.bunpu_gene([1.5],[5.0],[4.0],[1.0],[100],gegg=[0,0], volume=6000)
willsellratio.bunpu_graph('willsellratio',shw=1, fs=36)

#製品化コスト
#コスト＝(設備費-売上累積*0.2)/個数+材料費
facil=Bunpu()#設備費
facil.bunpu_gene([250],[500],[325],[40],[100],gegg=[0,0])
facil.bunpu_graph('facility', fs=36)
mater=Bunpu()#材料費
mater.bunpu_gene([1.2],[2.5],[1.8],[0.3],[100],gegg=[0,0])
mater.bunpu_graph('mater', fs=36)
jikei0=[]
jikei1=[]
jikei2=[]
zei=[]
for i in range(3):
    print(i)
    #初期企画個数
    if i == 0:
        num=[100]
        facil1=facil.bunpu_division(num)
        facil1.bunpu_graph('facilitycost', fs=36)
        cost=facil1.bunpu_add(mater)
         
    else:
        if kakaku!=0:
            num=[int(uriage/kakaku)]
        else:
            num=[1]
        if np.max(facil.para[0])>uriage and num[0]>1:
            if num == [0]:
                num = [1]
            uriage0 = 0.2*uriage
            facil0=facil.bunpu_sub([uriage0])
            facil1=facil0.bunpu_division(num)
            facil1.bunpu_graph('facilitycost', fs=36)
            cost=facil1.bunpu_add(mater)
        else:
            cost=mater
    cost.bunpu_graph('cost'+str(i), fs=36)
    
    jikei0.append(num)
    #供給分布
    
    supply = cost.bunpu_product(willsellratio)
    supply.bunpu_graph('supply'+str(i),shw=1, fs=36)
    
    #需給バランス曲線
    kakaku,uriage = demand.bunpu_balance(supply,'balance1'+str(i),dirc=[-1,1],shw=1, fs=36)
    jikei1.append(kakaku)
    jikei2.append(uriage)#
    zei.append(uriage*0.232)
fig=plt.figure(figsize=(14,7))
ax = fig.add_subplot(111)
outgraphname='jikei.png'
ax.plot(jikei0, label="num",color="green",linewidth = 4.0)
ax.plot(jikei1, label="kakaku",color="blue",linewidth = 4.0)
ax.plot(jikei2, label="uriage",color="red",linewidth = 4.0)
plt.rcParams["font.size"] = 36
ax.legend()
plt.savefig(outgraphname)
fig=plt.figure(figsize=(14,7))
ax = fig.add_subplot(111)
outgraphname='zei.png'
ax.plot(zei, label="houjinzei",color="green",linewidth = 4.0)
plt.rcParams["font.size"] = 36
ax.legend()
plt.savefig(outgraphname)
plt.close()
