import requests
import json
import os
import inspect
from .GetData import gettheuserid
from .install import installdatakund,checkifinstall
from .Progress import show_progress
from .GetAttributes import make_a_empty_class
import threading
global serverurl,global_user
serverurl="http://127.0.0.1:5350/"
folder=inspect.getfile(gettheuserid).split("site-packages")[0]
folder=folder+"site-packages\\bot_studio\\"
serverurl=checkifinstall(folder)
if(serverurl==" "):
    print("It currently works on windows only")
def changebotname(bot):
    prev=''
    newname=''
    for char in bot:
        if(prev=='_'):
            newname=newname+char.upper()
        else:
            newname=newname+char
        prev=char
    first=newname[0].upper()
    newname=newname[1:]
    newname=first+newname
    return newname
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
def fetch_the_response(name,res,user,bot,indexnumber,serverurl):
    res=make_a_empty_class(name,res,user,bot,indexnumber,serverurl)
    return res
def call_element_functions(self,index,name,args):
    global serverurl
    api_dict={"click":"click_on_element","find_element":"find_element","send_keys":"send_keys","wait_for_element":"find_element","find_elements":"find_element"}
    try:
        api=api_dict[name]
    except:
        api=name
    if(name.startswith("find_element") or name.startswith("wait_for_element")):
        self.bot=args['0']
    headers = {'Content-type': 'application/json'}
    args['indexnumber']=index
    args['bot']=self.bot
    args['user']=self.user
    args["tech_type"]="PIP"
    args["single_element"]=False
    if(name in ["find_element","wait_for_element"]):
        args["single_element"]=True
    res=requests.post(url=serverurl+api, data = json.dumps(args), headers=headers)
    try:
        res=json.loads(res.text)
    except:
        res=res.text
    if(name in ["find_element","find_elements","wait_for_element"]):
        res=fetch_the_response(name,res,self.user,self.bot,index,serverurl)
    return res
def modify_res(res,bot_name):
    resume_dict={}
    res_copy=res.copy()
    for bot in res_copy:
        if(bot not in ["body","errors","success_score"]):
            try:
                resume_dict[bot]=res[bot]["resume_variable"]
                del res[bot]["resume_variable"]
            except:
                pass
        elif(bot=="resume_variable"):
            resume_dict[bot_name]=res[bot]
            del res[bot]
    res["resume_dict"]=resume_dict
    return res
class bot_studio():
    def __init__(self):
        global global_user
        global_user=gettheuserid()
    def install(self):
        installdatakund()
    def use(self,link):
        global serverurl
        serverurl=link
    def __getattr__(self, name):
        def startbrowser(self,browseroptions):
            global serverurl
            if(serverurl==" "):
                print("It currently works on windows only")
                return 1
            startapi=serverurl+"startbrowser"
            headers = {'Content-type': 'application/json'}
            browseroptions["tech_type"]="PIP"
            res=requests.post(url = startapi, data = json.dumps(browseroptions), headers=headers)
            res=res.text
            res=json.loads(res)
            index=res["indexnumber"]
            if("message" in res):
                if(res["message"]!=""):
                    print(res["message"])
            return index
        def method(*argss,**kwargs):
            args=getargs(argss,kwargs,"")
            def callthefunction(self,index,name,args,bot):
                global serverurl
                if(name=="quit"):
                    try:
                        requests.get(serverurl+"quitdatakund")
                    except:
                        pass
                    os._exit(0)
                    return None
                if(serverurl==" "):
                    print("It currently works on windows only")
                    return 1
                url=serverurl+name
                headers = {'Content-type': 'application/json'}
                args['indexnumber']=index
                args['bot']=bot
                args['user']=self.user
                args["tech_type"]="PIP"
                res=requests.post(url = url, data = json.dumps(args), headers=headers)
                try:
                    res=json.loads(res.text)
                except:
                    res=res.text
                return res
            def set_browser_index(self,*argss,**kwargs):
                global global_user
                browseroptions=getargs(argss,kwargs,"")
                indexnumber=startbrowser(self,browseroptions)
                self.index=indexnumber
                self.domain=name
                try:
                    self.user=browseroptions["apiKey"]
                    self.private_bot=True
                except:
                    self.user=global_user
                    self.private_bot=False
            def __getattrr__(self, name):
                indexname=self.index
                def method(*argss,**kwargs):
                    if(name in ["end","get_snapshot","get_page_title","get_page_source","get_current_url","reload","keypress","open","scroll","getresponse","send_feedback","quit","refresh"]):
                        args=getargs(argss,kwargs,"")
                        method=callthefunction(self,indexname,name,args,'')
                    elif(name in ["click","find_element","find_elements","send_keys","wait_for_element"]):
                        args=getargs(argss,kwargs,"")
                        method=call_element_functions(self,indexname,name,args)
                    else:
                        args=getargs(argss,kwargs,"datakund")
                        domainname=self.domain
                        bot=name
                        if(domainname=="" or domainname=="new"):
                            bot=bot
                        else:
                            bot=domainname+"_"+bot
                        if("apiKey" in args or self.private_bot==True):
                            pass
                        else:
                            bot=bot+"~D75HsPTUIeOmN0bLp5ulrwB7F1f2"
                        def runbot(bot,outputdata):
                            global global_user ,serverurl
                            current_user=self.user
                            if(serverurl==" "):
                                print("It currently works on windows only")
                                return 
                            url1=serverurl+"datakundapi"
                            headers = {'Content-type': 'application/json'}
                            try:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"fields":outputdata["fields"],"tech_type":"PIP"}
                            except:
                                api_data={"user":current_user,"bot":bot,"indexnumber":self.index,"outputdata":outputdata,"tech_type":"PIP"}
                            if("apiKey" in outputdata):
                                current_user=outputdata["apiKey"]
                                api_data["user"]=outputdata["apiKey"]
                                api_data["privatebot"]=True
                            if(self.private_bot==True):
                                api_data["privatebot"]=True
                            if("data_format" in outputdata):
                                api_data["data_format"]=outputdata["data_format"]
                            if("resume_dict" in outputdata):
                                api_data["resume_dict"]=outputdata["resume_dict"]
                            start_time = threading.Timer(3,show_progress, args=(current_user,bot,self.index,serverurl+"fetchbotprogress",))
                            start_time.start()
                            res=requests.post(url = url1, data = json.dumps(api_data), headers=headers)
                            res=json.loads(res.text)
                            self.bot=bot
                            try:
                                self.body=res['body']
                            except:
                                self.body={}
                            try:
                                self.score=res['score']
                            except:
                                self.score=bot
                            try:
                                self.errors=res['errors']
                            except:
                                self.errors=[]
                            res=modify_res(res,bot)
                            return res
                        method=runbot(bot,args)
                    return method
                return method
            if(name=="quit"):
                try:
                    requests.get(serverurl+"quitdatakund")
                except:
                    pass
                return None
            elif(name=="send_feedback"):
                callthefunction(self,1,name,args,'')
                return "Thanks for your feedback!!"
            dynamicclass = type(name, 
              (), 
              { 
               "__init__": set_browser_index,
               "__getattr__":__getattrr__})
            obj1=dynamicclass(*argss,**kwargs)
            return obj1
        return method