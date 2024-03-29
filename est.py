# 平均的な物理量(主にself.vc)を可視化するプログラム

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import R2D2
import sys, os
import pickle

caseid = R2D2.util.caseid_select(locals()) # caseidを選択
datadir="../run/"+caseid+"/data/"

# 生成された画像の出力先の設定・作成
pngdir="../figs/"+caseid+"/est/"
os.makedirs(pngdir,exist_ok=True)

# R2D2 instanceの設定
R2D2.util.initialize_instance(locals(),'d')
d = R2D2.R2D2_data(datadir,self_old=d)
R2D2.util.locals_define(d,locals())
n0 = R2D2.util.define_n0(d,locals())

print("Maximum time step= ",d.p['nd']," time ="\
      ,d.p['dtout']*float(d.p['nd'])/3600./24.," [day]")

plt.close('all')

# vs codeでエラーを出さないために以下は定義
# 実際はR2D2.util.locals_defineで定義されている
ix, jx, nd = d.p['ix'], d.p['jx'], d.p['nd']

# 座標のファクターの設定
if d.p['geometry'] == 'Cartesian':
    sinyy = 1
    sinyym = 1.
else: # spherical geometry
    xx,yy = np.meshgrid(d.p['x'],d.p['y'],indexing='ij')
    sinyy = np.sin(yy)
    sinyym = np.average(sinyy,axis=1)

    xx,yy_flux = np.meshgrid(d.p['x_flux'],d.p['y'],indexing='ij')
    sinyy_flux = np.sin(yy_flux)
    sinyym_flux = np.average(sinyy_flux,axis=1)

# ここで計算した物理量は辞書型mdに入れていく
md = {}
# zerosの設定
## RMS and mean values
vls = ['vxrmst', 'vyrmst', 'vzrmst', 
        'bxrmst', 'byrmst', 'bzrmst',
        'rormst', 'sermst', 'prrmst', 'termst',
        'romt', 'semt', 'prmt', 'temt'
        ]
for vl in vls:
    md[vl] = np.zeros((ix, nd-n0+1))

## mean magnetic field (2D)
vls = ['vxmt', 'vymt', 'vzmt', 'bxmt', 'bymt', 'bzmt']
for vl in vls:
    md[vl] =  np.zeros((ix,jx,nd-n0+1))

## energy fluxes (1D but ix + 1)
vls = ['fet','fmt','fdt','fkt','frt','ftt','fft']
for vl in vls:
    md[vl] = np.zeros((ix+1,nd-n0+1))

###############################################################################
###############################################################################
###############################################################################
def est_plot(d, md, fig, ax1, ax2, ax3, ax4):    
    #####################
    if d.p['geometry'] == 'Cartesian':
        xp = (d.p['x_flux'] - d.p['rstar'])*1.e-8
        xpp = (d.p['x'] - d.p['rstar'])*1.e-8
        xlabel = r'$x-R_*~\mathrm{[Mm]}$'
    else:
        xp = d.p['x_flux']/d.p['rstar']
        xlabel = r'$r/R_*$'
        xpp = d.p['x']/d.p['rstar']
        
    if d.p['deep_flag'] == 0:
        text = r"$t="+"{:.2f}".format(t/60.)+"\mathrm{~[min]}$"
    else:
        text = r"$t="+"{:.2f}".format(t/3600./24.)+"\mathrm{~[day]}$"
    #####################
    # drawing
    vls = ['ff','fk','fr','fm','ft']
    colors = [R2D2.magenta,R2D2.green,R2D2.blue,R2D2.orange,R2D2.ash]
    labels = ['$F_\mathrm{e}$',r'$F_\mathrm{k}$',r'$F_\mathrm{r}$',r'$F_\mathrm{m}$',r'$F_\mathrm{t}$']
    for vl, color, label in zip(vls, colors, labels):
        ax1.plot(xp,md[vl]/fstar,label=label,color=color)

    ax1.hlines(y=1,xmin=xp.min(),xmax=xp.max(),linestyle='--',color=R2D2.ash)

    #####################
    md['vhrms'] = np.sqrt(md['vyrms'] + md['vzrms']**2)
    md['vvrms'] = np.sqrt(md['vxrms']**2 + md['vhrms']**2)
    vls = ['vxrms','vhrms','vvrms']
    colors = [R2D2.blue,R2D2.magenta,R2D2.green]
    labels = [r'$v_{x\mathrm{(rms)}}$',r'$v_\mathrm{h(rms)}$',r'$v_\mathrm{(rms)}$']
    for vl, color, label in zip(vls, colors, labels):
        ax2.plot(xpp,md[vl]*1.e-5,label=label,color=color)

    if d.p['deep_flag'] == 0:
        ax2.set_yscale('log')

    #####################
    md['bhrms'] = np.sqrt(md['byrms']**2 + md['bzrms']**2)
    md['bbrms'] = np.sqrt(md['bxrms']**2 + md['bhrms']**2)
    vls = ['bxrms','bhrms','bbrms']
    colors = [R2D2.blue,R2D2.magenta,R2D2.green]
    labels = [r'$B_{x\mathrm{(rms)}}$',r'$B_\mathrm{h(rms)}$',r'$B_\mathrm{(rms)}$']
    for vl, color, label in zip(vls, colors, labels):
        ax3.plot(xpp,md[vl]*1.e-5,label=label,color=color)
    
    #####################
    ax4.plot(xpp,md['sem']+d.p['se0'],color=R2D2.blue,label=r'$s$')
    ax4.plot(xpp,d.p['se0'],color=R2D2.blue,ls='--',label=r'$s_0$')

    titles = ['Energy fluxes','RMS velocity','RMS magnetic field','Entropy']
    ylabels = [r"$F/F_*$",r"velocities$\mathrm{~[km~s^{-1}]}$",r"Magnetic field [G]",r'$\mathrm{erg~g^{-1}~K^{-1}}$']
    for ax, ylabel, title in zip([ax1,ax2,ax3,ax4],ylabels,titles):
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(frameon=False,ncol=3,loc='upper left',fontsize=15)

    ax3.annotate(text=text,xy=[0.01,0.01],xycoords="figure fraction")

    # est_plot end
###############################################################################
###############################################################################
###############################################################################

for n in tqdm(range(n0,nd+1)):
    print(f"\r n = {n} ", end='', flush=True)
    ##############################
    t = d.read_time(n)    
    d.read_vc(n,silent=True)

    ##############################    
    if d.p['geometry'] == 'Cartesian':
        fstar = d.p['lstar']/4/np.pi/d.p['rstar']**2
        vls = ['fe','fd','fk','fr','fm']
        for vl in vls:
            md[vl] = np.average(d.vc[vl],axis=1)
    else:
        fstar = d.p['lstar']/4/np.pi
        vls = ['fe','fd','fk','fm']
        for vl in vls:
            md[vl] = np.average(d.vc[vl]*sinyy_flux,axis=1)/sinyym_flux*d.p['x_flux']**2
        md['fr'] = np.average(d.vc["fr"]*sinyy_flux,axis=1)/sinyym_flux#*x_flux**2
    
    # linear と full　の判別のためのRMSエントロピーの計算
    serms = np.sqrt(np.average(d.vc['serms']**2*sinyy,axis=1)/sinyym)/d.p['se0']
    sermsm = 0.5*(np.append(serms,serms[-1]) + np.insert(serms,0,serms[0]))
    sr = 0.5*(1 + np.sign(sermsm - 1.e-4))
    
    # fe: linear expression
    # fd: full expression
    md['ff'] = md['fd']*sr + md['fe']*(1.e0-sr)
    md['ft'] = md['ff'] + md['fk'] + md['fr'] + md['fm']

    # RMS values
    vls = ['vxrms','vyrms','vzrms','bxrms','byrms','bzrms','rorms','serms','prrms','terms']
    for vl in vls:
        md[vl+'t'][:,n-n0] = np.sqrt(np.average(d.vc[vl]**2*sinyy,axis=1)/sinyym)

    # energy flux
    vls = ['fe','fm','fd','fk','fr','ft','ff']
    for vl in vls:
        md[vl+'t'][:,n-n0] = md[vl]
        
    # mean magnetic field
    vls = ['vxm','vym','vzm','bxm','bym','bzm']
    for vl in vls:
        md[vl+'t'][:,:,n-n0] = d.vc[vl]

    # 平均量の取得
    vls = ['rom','sem','prm','tem']
    for vl in vls:
        md[vl+'t'][:,n-n0] = np.average(d.vc[vl]*sinyy,axis=1)/sinyym

    vls = ['vxrms','vyrms','vzrms','bxrms','byrms','bzrms','sem']
    for vl in vls:
        md[vl] = md[vl+'t'][:,n-n0]
        
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, num='est', figsize=(12, 8))

    est_plot(d,md,fig,ax1,ax2,ax3,ax4)

    if n == n0:
        fig.tight_layout()
    
    plt.pause(0.1)
    fig.savefig(pngdir+"py"+'{0:08d}'.format(n)+".png")

    if n != nd:
        plt.clf() # clear figure
    
    # loop end
    ###############################################################################

vls = ['vxrms','vyrms','vzrms',
       'bxrms','byrms','bzrms',
       'rorms','serms','prrms','terms'
       ]
for vl in vls:
    md[vl] = np.sqrt(np.average(md[vl+'t']**2,axis=1))

vls = ['rom','sem','prm','tem']
for vl in vls:
    md[vl] = np.average(md[vl+'t'],axis=1)

vls = ['fe','fd','ff','fk','fr','ft']
for vl in vls:
    md[vl] = np.average(md[vl+'t'],axis=1)

with open(d.p['datadir']+'est.pkl','wb') as f:
    pickle.dump([d.p,md], f)    

fig2, ((ax21, ax22), (ax23, ax24)) = plt.subplots(2, 2, num='est_mean', figsize=(12, 8))
est_plot(d,md,fig2,ax21,ax22,ax23,ax24)
fig2.tight_layout()