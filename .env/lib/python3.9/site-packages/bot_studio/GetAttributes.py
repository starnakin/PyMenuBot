import json
import requests
def getargs(argss,kwargs,api):
    if(api=="datakund" and len(argss)>0):
        args=list(argss)
        return args
    args={}
    i=0
    for a in argss:
        args[str(i)]=a
        i=i+1
    args.update(kwargs)
    return args
def make_request(self,func_name,args):
    api_dict={"click":"click_on_element","find_element":"find_element","find_elements":"find_element","send_keys":"send_keys_to_element","wait_for_element":"find_element"}
    try:
        api=api_dict[func_name]
    except:
        api=func_name
    headers = {'Content-type': 'application/json'}
    args['indexnumber']=self.indexnumber
    args['bot']=self.bot
    args['user']=self.user
    args['element_number']=self.element_number
    if(func_name=="wait_for_element"):
        args['wait_for_element']=True
        args['wait_time']=args['1']
    serverurl=self.serverurl
    res=requests.post(url=serverurl+api, data = json.dumps(args), headers=headers)
    try:
        res=json.loads(res.text)
    except:
        res=res.text
    return res
class empty_class():
    def __init__(self,text,element_number,user,bot,indexnumber,serverurl):
        self.text=text
        self.user=user
        self.bot=bot
        self.element_number=element_number
        self.indexnumber=indexnumber
        self.serverurl=serverurl
    def __getattr__(self,func_name):
        def method(*argss,**kwargs):
            args=getargs(argss,kwargs,"")
            res=make_request(self,func_name,args)
            return res
        return method
def make_a_empty_class(name,res,user,bot,indexnumber,serverurl):
    if(name in ["find_element","wait_for_element"]):
        clas=empty_class(res["0"],0,user,bot,indexnumber,serverurl)
        return clas
    lst=[]
    for i in res:
        obj=empty_class(res[i],int(i),user,bot,indexnumber,serverurl)
        lst.append(obj)
    return lst