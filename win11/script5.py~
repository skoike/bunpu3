# -*- coding: utf-8 -*-
#bunpu2用のシミュレーション
from bunpu import *
dlt0 = 0.01
tm=400#120km/hの場合
#tm=800#60km/hの場合
dim=1

#運動方程式
#|dr| |A B||r| |E|
#|  |=|   || |+| |s
#|db| |C D||b| |F|

Kf=36500.0#*0.3#N/rad
Kr=36500.0#*0.3#N/rad
lf=1.0
lr=1.6
Iz=1470#kgm
m=1200#kg

lff=1.6
lrr=2.4
#w=0.8
w=1.5
ka=0.5
kd=2
kc=0.1
kb=1.0#laに比例して操舵戻す、
ke = 0.5#yに比例して操舵戻す
kfr0=bunpu()#コーナリングパワー
#kfr0.bunpu_gene([36000],[36900],[36500],[120],[100])
kfr0.bunpu_gene([31900],[32800],[32100],[200],[100])#case1
#kfr0.bunpu_gene([31900],[32800],[32100],[150],[100])#case2
kfr0.bunpu_graph('corner_power',fs=24)
kfr1=bunpu()#コーナリングパワー4~8deg
kfr1.bunpu_gene([15950],[16400],[15150],[200],[100])#case1
kfr2=bunpu()#コーナリングパワー8~deg
kfr2.bunpu_gene([100],[500],[250],[200],[100])#case1
tgt_s=bunpu()
#tgt_s0=bunpu_gene([-0.3],[0.3],[0],[0.1],[20])#目標だ角deg
tgt_s.vector_gene([0])
lasts=bunpu()
lasts=tgt_s
dd0=bunpu()
#dd0.bunpu_gene([60],[80],[67],[3],[50])#検出距離
#dd0.bunpu_gene([40],[60],[57],[3],[100])#検出距離case1
#dd0.bunpu_gene([40],[60],[45],[3],[100])#case2
dd0.bunpu_gene([40],[60],[50],[3],[100])#case3
dd0.bunpu_graph('detect_dist',fs=24)
#障害物初期位置
distd=100
la0=bunpu()
la0.vector_gene([0])
r0=bunpu()
r0.vector_gene([0])
b0=bunpu()
b0.vector_gene([0])
#x0=bunpu()
#x0.vector_gene([0])
x0=0
y0=bunpu()
y0.vector_gene([0])
la=la0
r1=r0
b1=b0
x1=x0
y1=y0
minidist=[]
#タイヤスリップ角の初期値
af=0
ar=0
#v0=bunpu()
#v0.vector_gene([60*1000/3600])#m/s
#v0=60*1000/3600#m/s
v0=120*1000/3600#m/s
r1list=[]
r2list=[]
b1list=[]
b2list=[]
dr1list=[]
dr2list=[]
db1list=[]
db2list=[]
la1list=[]
la2list=[]
s11list=[]
s12list=[]
s21list=[]
s22list=[]
st1list=[]
st2list=[]
xlist=[]
y1list=[]
y2list=[]
cond1list=[]
cond2list=[]
af1list=[]
af2list=[]
ar1list=[]
ar2list=[]

for t in range(tm):

    #バラツキ要素は以下の2つとする
    # kfr:コーナリングパワー
    # dd:障害物検出距離
    #積分パラメータ
    # la,r,dr:ヨー角、ヨーレイト
    # b,db:スリップ角
    # x,dx:前後位置
    # y,dy:横位置
    #制御パラメータ
    # tgt_s:操舵角
    #
    #kfr = bunpu()
    #dd = bunpu()
    kfr,dd = kfr0.bunpu_simu_start([dd0],dlt=dlt0,shw=1)
    #K,tgt_sからdr,dbの作成
    #breakpoint()
    if t == 0:
        kr = kfr
        kf = kfr
    else:
        #
        condf = np.ones((kfr.linemap[0][3].shape))
        #breakpoint()
        #condf10 = af.bunpu_simu_comp([-4,4],2)
        #condf20 = af.bunpu_simu_comp([-8,8],2)
        condf10 = af.bunpu_simu_comp([-2,2],2)
        condf20 = af.bunpu_simu_comp([-4,4],2)
        condf1 = condf-condf20+condf10*0.5+(condf20-condf10)*0.01
        kf = kfr
        kf.linemap[0][3] = kfr.linemap[0][3]*condf1
        #condr11 = ar.bunpu_simu_comp([-4,4],2)
        #condr21 = ar.bunpu_simu_comp([-8,8],2)
        condr11 = ar.bunpu_simu_comp([-2,2],2)
        condr21 = ar.bunpu_simu_comp([-4,4],2)
        condr2 = condf-condr21+condr11*0.5+(condr21-condr11)*0.01
        kr = kfr
        kr.linemap[0][3] = kfr.linemap[0][3]*condr2
    
    #運動方程式
    #A=-(2*kfr*lf**2+2*kfr*lr**2)/(Iz*v0)
    #breakpoint()
    #
    k1=kf.bunpu_simu_prd(-2*lf**2/(Iz*v0))
    k2=kr.bunpu_simu_prd(-2*lr**2/(Iz*v0))
    A=k1.bunpu_simu_add(k2)
    #B=-(2*kfr*lf-2*kfr*lr)/Iz
    k3=kf.bunpu_simu_prd(-2*lf/Iz)
    k4=kr.bunpu_simu_prd(2*lr/Iz)
    B=k3.bunpu_simu_add(k4)
    #C=-(1+(2*kfr*lf-2*kfr*lr)/(m*v0**2))
    k5=kf.bunpu_simu_prd(-2*lf/(m*v0**2))
    k6=kr.bunpu_simu_prd(2*lr/(m*v0**2))
    k7=k5.bunpu_simu_add(k6)
    C=k7.bunpu_simu_sub(1/(m*v0**2))
    #D=-(2*kfr+2*kfr)/(m*v0)
    k8=kf.bunpu_simu_prd(-2/(m*v0))
    k9=kr.bunpu_simu_prd(-2/(m*v0))
    D=k8.bunpu_simu_add(k9)
    #E=2*kfr*lf/Iz
    E=kf.bunpu_simu_prd(2*lf/Iz)
    #F=2*kfr/(m*v0)
    F=kf.bunpu_simu_prd(2/(m*v0))
    
    #dr=A*r+B*b+E*tgt_s
    k10=A.bunpu_simu_prd(r1)
    k11=B.bunpu_simu_prd(b1)
    k12=E.bunpu_simu_prd(tgt_s)
    k13=k10.bunpu_simu_add(k11)
    #dr=k13.bunpu_simu_add(k12)
    #ヨーレートの変化率を50以下に制限
    dr0=k13.bunpu_simu_add(k12)
    dr=dr0.bunpu_simu_limit([np.pi*30/180])
    #db=C*r+D*b+F*tgt_s
    k14=C.bunpu_simu_prd(r1)
    k15=D.bunpu_simu_prd(b1)
    k16=F.bunpu_simu_prd(tgt_s)
    k17=k14.bunpu_simu_add(k15)
    db=k17.bunpu_simu_add(k16)
    
    #rn= r+dr*dt
    #bn= b+db*dt
    #breakpoint()
    #3/10selfとotherを逆にする
    r1=r0.bunpu_simu_integral([dr],dlt0,shw=1)
    b1=b0.bunpu_simu_integral([db],dlt0,shw=1)
    
    #lan= la+r*dt
    la=la0.bunpu_simu_integral([r1],dlt0,shw=1)
    
    #xn= x+v0*dt
    #yn= y+v0*(la-b)*dt
    #x=x0.bunpu_simu_integral([v0],dlt0,shw=1)
    x=x0+v0*dlt0
    #dy=v0*(la-b1)
    k18=la.bunpu_simu_sub(b1)
    k19=k18.bunpu_simu_prd(v0)
    y=y0.bunpu_simu_integral([k19],dlt0,shw=1)
    
    x0=x
    y0=y
    r0=r1
    b0=b1
    la0=la
    r1list.append(np.min(r1.linemap[0][3]*180/np.pi))
    r2list.append(np.max(r1.linemap[0][3]*180/np.pi))
    b1list.append(np.min(b1.linemap[0][3]*180/np.pi))
    b2list.append(np.max(b1.linemap[0][3]*180/np.pi))
    dr1list.append(np.min(dr.linemap[0][3]*180/np.pi))
    dr2list.append(np.max(dr.linemap[0][3]*180/np.pi))
    db1list.append(np.min(db.linemap[0][3]*180/np.pi))
    db2list.append(np.max(db.linemap[0][3]*180/np.pi))
    #lalist.append(la*180/np.pi)
    #slist.append(s*180/np.pi)
    xlist.append(x)
    y1list.append(np.min(y.linemap[0][3]))
    y2list.append(np.max(y.linemap[0][3]))

    #cond0=dd<distd#TypeError: '<' not supported between instances of 'bunpu' and 'int'
    #cond1 = (distd-x).bunpu_simu_comp([dd,5],3)
    #cond2 = (distd-x).bunpu_simu_comp([dd,5],2)
    #breakpoint()
    cond1 = dd.bunpu_simu_comp([distd-x,5],5)
    cond2 = dd.bunpu_simu_comp([distd-x,5],4)
    
    #ターゲットあり
    
    #s1 = ka*(np.arctan((w+kd-y)/(distd-x))-la)
    k20 = y.bunpu_simu_sub(w+kd)
    k21 = k20.bunpu_simu_div(x-distd)
    k22 = k21.bunpu_simu_arctan()
    k23 = k22.bunpu_simu_sub(la)
    
    k24 = k23.bunpu_simu_prd(ka)
    s1 = k24.bunpu_simu_limit([np.pi*30/180])
    #breakpoint()
    #ターゲットなし
    #s2 = -kb*la
    k25 = la.bunpu_simu_prd(-1*kb)
    #k30 = y.bunpu_simu_prd(-1*ke)
    #k31 = k25.bunpu_simu_add(k30)
    #s2 = k31.bunpu_simu_limit([np.pi*30/180])
    s2 = k25.bunpu_simu_limit([np.pi*30/180])
    
    #操舵角
    #tgt_s=s1*cond1+s2*cond2
    k26 = s1.bunpu_simu_prd(cond1)
    k27 = s2.bunpu_simu_prd(cond2)
    k28 = k26.bunpu_simu_add(k27)
    k29 = k28.bunpu_simu_limitspd(lasts,[30*np.pi/180])
    tgt_s = k29.bunpu_simu_limit([np.pi*30/180])
    lasts = copy.deepcopy(tgt_s)
    cond1list.append(np.sum(cond1))
    cond2list.append(np.sum(cond2))
    s11list.append(np.min(s1.linemap[0][3]*180/np.pi))
    s12list.append(np.max(s1.linemap[0][3]*180/np.pi))
    s21list.append(np.min(s2.linemap[0][3]*180/np.pi))
    s22list.append(np.max(s2.linemap[0][3]*180/np.pi))
    st1list.append(np.min(tgt_s.linemap[0][3]*180/np.pi))
    st2list.append(np.max(tgt_s.linemap[0][3]*180/np.pi))
    la1list.append(np.min(la.linemap[0][3]*180/np.pi))
    la2list.append(np.max(la.linemap[0][3]*180/np.pi))
    print(t)
    #タイヤのスリップ角を演算
    atmp=r1.bunpu_simu_prd(lf/v0)
    aftmp = b1.bunpu_simu_add(atmp)
    af = tgt_s.bunpu_simu_sub(aftmp)
    #ar = lr-b1
    artmp = r1.bunpu_simu_prd(lr/v0)
    ar = artmp.bunpu_simu_sub(b1)
    af1list.append(np.min(af.linemap[0][3])*180/np.pi)
    af2list.append(np.max(af.linemap[0][3])*180/np.pi)
    ar1list.append(np.min(ar.linemap[0][3])*180/np.pi)
    ar2list.append(np.max(ar.linemap[0][3])*180/np.pi)
    #if x>=94:
    #    breakpoint()
    #障害物との位置関係を表示
    #baria=[[distd,w],[distd,-1*w],[distd+5,-1*w],[distd+5,*w]]
    distd5=distd+5
    baria=[[distd5,distd,distd,distd5],[w,w,-1*w,-1*w]]
    #baria2=[[0,0,100,120,140,140],[15,7,7,7,7,15]]
    baria2=[[0,0,140,140],[15,7,7,15]]
    #breakpoint()
    #車両の四隅とヨー角を指示
    cosla=la.bunpu_simu_cos()
    sinla=la.bunpu_simu_sin()
    lfs0=sinla.bunpu_simu_prd(lf)
    lfc0=cosla.bunpu_simu_prd(lf)
    ws0=sinla.bunpu_simu_prd(w)
    wc0=cosla.bunpu_simu_prd(w)
    xrf0=lfc0.bunpu_simu_sub(ws0)
    xrf=xrf0.bunpu_simu_add(x)#
    yrf0=lfs0.bunpu_simu_sub(wc0)
    yrf=y.bunpu_simu_sub(yrf0)#
    xlf0=lfc0.bunpu_simu_add(ws0)
    xlf=xlf0.bunpu_simu_add(x)#
    ylf0=lfs0.bunpu_simu_add(wc0)
    ylf=y.bunpu_simu_sub(ylf0)#
    #
    lrs0=sinla.bunpu_simu_prd(lr)
    lrc0=cosla.bunpu_simu_prd(lr)
    xrr0=lrc0.bunpu_simu_add(ws0)
    xrr0m=xrr0.bunpu_simu_prd(-1)
    xrr=xrr0m.bunpu_simu_add(x)#
    yrr0=wc0.bunpu_simu_sub(lrs0)
    yrr=y.bunpu_simu_add(yrr0)#
    xlr0=ws0.bunpu_simu_sub(lrc0)
    xlr=xlr0.bunpu_simu_add(x)#
    ylr0=lrs0.bunpu_simu_add(wc0)
    ylr=y.bunpu_simu_sub(ylr0)#
    #車両の四隅最大最小端の位置
    #リヤレフトポイントのy最大値を１、リヤライトy最小値を２とする
    n1=np.unravel_index(np.argmax(ylr.linemap[0][3]),ylr.linemap[0][3].shape)
    n2=np.unravel_index(np.argmin(yrr.linemap[0][3]),yrr.linemap[0][3].shape)
    n3=np.unravel_index(np.argmax(ylf.linemap[0][3]),ylf.linemap[0][3].shape)
    n4=np.unravel_index(np.argmin(yrf.linemap[0][3]),yrf.linemap[0][3].shape)
    frpos1=[xrf.linemap[0][3][n1],yrf.linemap[0][3][n1]]
    flpos1=[xlf.linemap[0][3][n1],ylf.linemap[0][3][n1]]
    rrpos1=[xrr.linemap[0][3][n1],yrr.linemap[0][3][n1]]
    rlpos1=[xlr.linemap[0][3][n1],ylr.linemap[0][3][n1]]
    frpos2=[xrf.linemap[0][3][n2],yrf.linemap[0][3][n2]]
    flpos2=[xlf.linemap[0][3][n2],ylf.linemap[0][3][n2]]
    rrpos2=[xrr.linemap[0][3][n2],yrr.linemap[0][3][n2]]
    rlpos2=[xlr.linemap[0][3][n2],ylr.linemap[0][3][n2]]
    #
    #以下は、四隅の軌跡を求める
    #yosumi = [frpos,flpos,rrpos,rlpos]
    #
    y.bunpu_simu_graph([[frpos1,flpos1,rlpos1,rrpos1,frpos2,flpos2,rlpos2,rrpos2],baria,baria2],t,tm,'trace1',ratio=1, shape=[int(tm*7/10),int(tm*3/4)],fs=24)
    #y.bunpu_simu_graph([x,baria],t,tm,'trace0')
    #物体のバラツキ外縁をトレースする関数と、接触確率を演算する関数を完成させる。
    #以下は、軌跡（xrfポイント）が所定範囲（障害物存在範囲）に入る確率を求める
    flag0=2
    minidist=ylf.bunpu_simu_prb(xlf,[baria2,minidist],flag0,t,tm,'contactprb')#ylf,xlf:車両左前
    #minidist=ylf.bunpu_simu_prb(xlf,[baria,minidist],flag0,t,tm,'contactprb')

    #ループの終わり

