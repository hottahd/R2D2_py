import R2D2

caseid = R2D2.util.caseid_select(locals())
datadir="../run/"+caseid+"/data/"

try:
    d
except NameError:
    d = None
d = R2D2.R2D2_data(datadir,verbose=True,self_old=d)
R2D2.util.locals_define(d,locals())
