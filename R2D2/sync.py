import os

def set(server,caseid,project=os.getcwd().split('/')[-2],dist='../run/'):
    '''
    This method downloads setting data from remote server

    Parameters:
        server (str): name of remote server
        caseid (str): caseid format of 'd001'
        project (str): name of project such as 'R2D2'
        dist (str): distination of data directory
    '''
    import os
        
    os.system('rsync -avP' \
              +' --exclude="a.out" ' \
              +' --exclude=".git" ' \
              +' --exclude="make/*.o" ' \
              +' --exclude="make/*.lst" ' \
              +' --exclude="make/*.mod" ' \
              +' --exclude="data/qq" ' \
              +' --exclude="data/remap/qq" ' \
              +' --exclude="data/remap/vl/vl*" ' \
              +' --exclude="data/slice/qq*" ' \
              +' --exclude="data/tau/qq*" ' \
              +' --exclude="data/time/tau" ' \
              +server+':work/'+project+'/run/'+caseid+' '+dist)
    
def sync_tau(self,server,project=os.getcwd().split('/')[-2]):
    '''
    This method downloads data at constant optical depth

    Parameters:
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
    '''

    import os

    caseid = self.p['datadir'].split('/')[-3]
    os.system('rsync -avP' \
              +' --exclude="param" ' \
              +' --exclude="qq" ' \
              +' --exclude="remap" ' \
              +' --exclude="slice" ' \
              +' --exclude="time/mhd" ' \
              +server+':work/'+project+'/run/'+caseid+'/data/ '+self.p['datadir'] )
    
def sync_select(self,xs,server,project=os.getcwd().split('/')[-2]):
    '''
    This method downloads data at certain height

    Parameters:
        xs (float): height to be downloaded
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
    '''

    import os
    import numpy as np

    i0 = np.argmin(np.abs(self.p["x"]-xs))
    ir0 = self.p["i2ir"][i0]
    
    nps = np.char.zfill(self.p['np_ijr'][ir0-1,:].astype(np.str),8)

    files = ''
    caseid = self.p['datadir'].split('/')[-3]

    for np in nps:
        files = files + server+':work/'+project+'/run/'+caseid \
                +'/data/remap/qq/qq.dac.' + '"*".' + np + " "
    
    os.system('rsync -avP ' \
          +files \
          +' '+self.p['datadir']+'remap/qq/' )

def sync_vc(self,server,project=os.getcwd().split('/')[-2]):
    '''
    This method downloads pre analysed data

    Parameters:
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
    '''

    import os
    caseid = self.p['datadir'].split('/')[-3]
    os.system('rsync -avP' \
              +' --exclude="time/mhd" ' \
              +server+':work/'+project+'/run/'+caseid+'/data/remap/vl '
              +self.p['datadir']+'remap/' )

def sync_check(self,n,server,project=os.getcwd().split('/')[-2],end_step=False):
    '''
    This method downloads checkpoint data

    Parameters:
        n (int): step to be downloaded
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
        end_step (bool): If true, checkpoint of end step is read
    '''
    import numpy as np
    import os
    
    step = str(n).zfill(8)
    
    if end_step:
        if np.mod(self.p['nd'],2) == 0:
            step = 'e'
        if np.mod(self.p['nd'],2) == 1:
            step = 'o'
    
    caseid = self.p['datadir'].split('/')[-3]
    os.system('rsync -avP ' \
              +server+':work/'+project+'/run/'+caseid+'/data/qq/qq.dac.'+step+' ' \
              +self.p['datadir']+'qq/' )

def sync_slice(self,server,project=os.getcwd().split('/')[-2]):
    '''
    This method downloads slice data

    Parameters:
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
    '''
    import numpy as np
    import os
    
    caseid = self.p['datadir'].split('/')[-3]
    os.system('rsync -avP ' \
              +server+':work/'+project+'/run/'+caseid+'/data/slice ' \
              +self.p['datadir'] )
        
def sync_all(self,server,project=os.getcwd().split('/')[-2],dist='../run/'):
    '''
    This method downloads all the data

    Parameters:
        server (str): name of remote server
        project (str): name of project such as 'R2D2'
        dist (str): distination of data directory
    '''
    import os
    
    caseid = self.p['datadir'].split('/')[-3]
    os.system('rsync -avP ' \
              +server+':work/'+project+'/run/'+caseid+' ' \
              +dist)


    
    
