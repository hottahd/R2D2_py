import os
import pyR2D2

class Sync:
    """
    Class for downloading data from remote server
    
    """
    
    def __init__(self, data):
        """
        Initialize pyR2D2.Sync
        
        Parameters
        ----------
        read : pyR2D2.Read
            Instance of pyR2D2.read
        """
        self.data = data
                
    def __getattr__(self, name):
        if hasattr(self.data, name):
            return getattr(self.data, name)

        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
    @staticmethod
    def setup(server,caseid,ssh='ssh',project=os.getcwd().split('/')[-2],dist='../run/'):
        '''
        Downloads setting data from remote server

        Parameters
        ----------
        server : str
            Name of remote server
        caseid : str
            caseid format of 'd001'
        ssh : str
            Type of ssh command
        project : str
            Name of project such as 'R2D2'
        dist :str
            Destination of data directory
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
                +' --exclude="output.*" ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/'+' '+dist+caseid+'/')
            
    def tau(self,server, n: int = None, ssh='ssh', project=os.getcwd().split('/')[-2]):
        '''
        Downloads data at constant optical depth

        Parameters
        ----------
        server : str
            Name of remote server
        ssh : str
            Type of ssh command
        project : str
            Name of project such as 'R2D2'
        '''

        import os
        
        if n is None:
            filedir = ''
            filename = ' '
        else:
            filename = 'tau/qq.dac.'+str(n).zfill(8)

        caseid = self.datadir.split('/')[-3]
        os.system('rsync -avP' \
                +' --exclude="param" ' \
                +' --exclude="qq" ' \
                +' --exclude="remap" ' \
                +' --exclude="slice" ' \
                +' --exclude="time/mhd" ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/'+filename+' '+self.datadir+filename )
        
    def remap_qq(self,n,server,ssh='ssh',project=os.getcwd().split('/')[-2]):
        '''
        Downloads full 3D remap data

        Parameters
        ----------
        n : int
            Target time step
        server : str
            Name of remote server
        project : str
            Name of project such as 'R2D2'
        ssh : str
            Type of ssh command
        '''
        import os
        import numpy as np
        
        caseid = self.datadir.split('/')[-3]
        
        # remapを行ったMPIランクの洗い出し
        nps = np.char.zfill(self.np_ijr.flatten().astype(str),8)
        for ns in nps:
            par_dir = str(int(ns)//1000).zfill(5)+'/'
            chi_dir = str(int(ns)).zfill(8)+'/'
            
            os.makedirs(self.datadir + 'remap/qq/'+par_dir+chi_dir,exist_ok=True)
            os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/remap/qq/'+par_dir+chi_dir+'qq.dac.'+str(n).zfill(8)+'.'+ns \
                    +' '+self.datadir + 'remap/qq/'+par_dir+chi_dir)
        
    def select(self,xs,server, n: int = None, ssh='ssh',project=os.getcwd().split('/')[-2]):
        '''
        Downloads data at certain height

        Parameters
        ----------
            xs : float
                Height to be downloaded
            server : str
                Name of remote server
            ssh : str
                Type of ssh command
            project : str
                Name of project such as 'R2D2'
        '''

        import os
        import numpy as np

        i0 = np.argmin(np.abs(self.x - xs))
        ir0 = self.i2ir[i0]
        
        nps = np.char.zfill(self.np_ijr[ir0-1,:].astype(str),8)

        files = ''
        caseid = self.datadir.split('/')[-3]
        
        if n is None:
            filename_part = 'qq.dac.*.'
        else:
            filename_part = 'qq.dac.'+str(n).zfill(8)+'.'

        for ns in nps:
            par_dir = str(int(ns)//1000).zfill(5)+'/'
            chi_dir = str(int(ns)).zfill(8)+'/'
            
            os.makedirs(self.datadir + 'remap/qq/'+par_dir+chi_dir,exist_ok=True)
            os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/remap/qq/'+par_dir+chi_dir+filename_part+ns \
                    +' '+self.datadir + 'remap/qq/'+par_dir+chi_dir)
            
    def vc(self,server,ssh='ssh',project=os.getcwd().split('/')[-2]):
        '''
        Downloads pre analyzed data

        Parameters
        ----------
        server : str
            Name of remote server
        ssh : str
            Type of ssh command
        project : str
            Name of project such as 'R2D2'
        '''

        import os
        caseid = self.datadir.split('/')[-3]

        pyR2D2.sync.setup(server,caseid,project=project)
        os.system('rsync -avP' \
                +' --exclude="time/mhd" ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/remap/vl '
                +self.datadir+'remap/' )
        
    def check(self,n,server,ssh='ssh',project=os.getcwd().split('/')[-2],end_step=False):
        '''
        Downloads checkpoint data

        Parameters
        ----------
        n : int
            Step to be downloaded
        server : str
            Name of remote server
        ssh : str
            Type of ssh command
        project : str
            Name of project such as 'R2D2'
        end_step : bool
            If true, checkpoint of end step is read
        '''
        import numpy as np
        import os
        
        step = str(n).zfill(8)
        
        if end_step:
            if np.mod(self.nd,2) == 0:
                step = 'e'
            if np.mod(self.nd,2) == 1:
                step = 'o'
        
        caseid = self.datadir.split('/')[-3]
        for ns in range(self.npe):
            par_dir = str(int(ns)//1000).zfill(5)+'/'
            chi_dir = str(int(ns)).zfill(8)+'/'

            os.makedirs(self.datadir + 'qq/'+par_dir+chi_dir,exist_ok=True)
            os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/qq/'+par_dir+chi_dir+'qq.dac.'+step+'.'+str(int(ns)).zfill(8)+' ' \
                +self.datadir + 'qq/'+par_dir+chi_dir )

    def slice(self,n,server,ssh='ssh',project=os.getcwd().split('/')[-2]):
        '''
        Downloads slice data

        Parameters
        ----------
        n : int
            Step to be downloaded
        server : str
            Name of remote server
        ssh : str
            Type of ssh command
        project : str
            Name of project such as 'R2D2'
        '''
        import numpy as np
        import os

        step = str(n).zfill(8)
        
        caseid = self.datadir.split('/')[-3]
        os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/slice/slice.dac ' \
                +self.datadir + '/slice' )
        os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/data/slice/qq"*".dac.'+step+'."*" ' \
                +self.datadir + '/slice' )
            
    def all(self,server,ssh='ssh',project=os.getcwd().split('/')[-2],dist='../run/'):
        '''
        This method downloads all the data

        Parameters
        ----------
        server : str
            Name of remote server
        ssh : str
            Type of ssh command
        project :str
            Name of project such as 'R2D2'
        dist :str
            Destination of data directory
        '''
        import os
        
        caseid = self.datadir.split('/')[-3]
        os.system('rsync -avP ' \
                +' -e "'+ssh+'" ' \
                +server+':work/'+project+'/run/'+caseid+'/ ' \
                +dist+caseid)
