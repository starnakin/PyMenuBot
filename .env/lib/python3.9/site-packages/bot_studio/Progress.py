from tqdm import tqdm
import requests
import time
import json
global progress_dict
progress_dict={}
def fetch_progress(user,bot,indexnumber,api):
    global progress_dict
    data={"user":user,"bot":bot,"indexnumber":indexnumber}
    headers = {'Content-type': 'application/json'}
    res=requests.post(url = api, data = json.dumps(data), headers=headers)
    res=res.text
    res=json.loads(res)
    progress_dict[user+bot+str(indexnumber)]=res
    return res["progress"]
def get_progress_dict(user,bot,indexnumber):
    try:
        prog_dict=progress_dict[user+bot+str(indexnumber)]
    except:
        prog_dict={}
    return prog_dict
def show_progress(user,bot,indexnumber,api):
    prog=5
    last=5
    with tqdm(total=200, desc="Progress") as progress:
        progress.update(10)
        while(prog!=100):
            last=prog
            prog=fetch_progress(user,bot,indexnumber,api)
            time.sleep(2)
            if(prog==0 or prog<=5):
                pass
            else:
                final=prog-last
                progress.update(final+final)
    progress.close()