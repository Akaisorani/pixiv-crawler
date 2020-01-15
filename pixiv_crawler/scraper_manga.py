#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['login','set_value','save_garage','dl_tag','dl_artist','dl_bookmark','dl_rank_global','dl_rank_daily','dl_rank_weekly','dl_rank_original','dl_rank_daily_r18','dl_rank_male_r18','dl_rank_weekly_r18','dl_diy_urls','random_one_by_classfi','get_value']
__author__ = "Akaisora"

import requests,json
import os,threading,datetime,sys,time,traceback
import random,re,copy
#import configparser
from html import unescape
from lxml import html
import pixiv_crawler.myconfig as config
from pixiv_crawler.login_sim import login_for_cookies

def login(save_cookies=True):
    if os.path.exists(config.cookies_file) :
        try:
            with open(config.cookies_file,"r") as f:
                cookies_js=json.load(f)
                cookiejar=requests.utils.cookiejar_from_dict(cookies_js, cookiejar=None, overwrite=True)
                session_requests.cookies=cookiejar
        except Exception as e:
            print("load cookies failed, try log in")
            traceback.print_exc()
    r=None
    try:
        r=session_requests.get(pixiv_root)
    except Exception as e:
        traceback.print_exc()
        print(e)
        
    if r is not None and r.status_code==200 and re.search('not-logged-in',r.text)==None:
        print("loaded cookies")
        return
    
    #check username & password
    if not config.username:raise Exception('Please set username')
    if not config.password:raise Exception('Please set password')
    
    
    # old login method, not work for captcha
    # login_url='https://accounts.pixiv.net/login'
    # r=session_requests.get(login_url)
    
    # tree=html.fromstring(r.text)
    # authenticity_token=list(set(tree.xpath("//input[@name='post_key']/@value")))[0]
    # payload={
        # 'pixiv_id':config.username,
        # 'password':config.password,
        # 'post_key':authenticity_token
    # }
    # r=session_requests.post(
        # login_url,
        # data=payload,
        # headers=dict(referer=login_url)
    # )
    
    print("try log in")
    cookies_dict=login_for_cookies(config)
    cookiejar=requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
    session_requests.cookies=cookiejar
    
    r=session_requests.get(pixiv_root)
    if re.search('not-logged-in',r.text)!=None:raise IOError('login failed, may deleting the cookies file can help')
    else:
        #print("log in")
        if save_cookies:
            with open(config.cookies_file,"w") as f:    #第一次登录后将存档cookies用来登录
                cookies_js = requests.utils.dict_from_cookiejar(session_requests.cookies)
                json.dump(cookies_js, f)

def downloadImage(imgurl,filename,*,header=None,imgid=None,imgidext=None):
    print("%s is downloading %s"%(threading.current_thread().name,filename))
    try:
        if header : r=session_requests.get(imgurl,headers=header,timeout=30)
        else : r=session_requests.get(imgurl,timeout=30)
        if r.status_code==200:
            try:
                write_rlock.acquire()
                with open(filename,'wb') as f:
                    f.write(r.content)
            finally:write_rlock.release()
        else:raise IOError('requestFailed')
    except Exception as e:
        print('FAIL %s failed to download %s'%(threading.current_thread().name,filename))
        if os.path.exists(filename) : os.remove(filename)
        faillog.append(filename)
        traceback.print_exc()
        return False
    else:
        print('SUCCESS %s has sucessfully downloaded %s'%(threading.current_thread().name,filename))
        try:
            garage_rlock.acquire()
            if imgidext:garage.add(imgidext)
            elif imgid:garage.add(imgid)
        finally:garage_rlock.release()
        return True

# def listener():
    # while(listen_active):
        # x=input()
        # if x=="q":
            # try:
                # garage_rlock.acquire()
                # if os.path.exists(config.garage_file) :
                    # with open(config.garage_file,"r") as f:
                        # garage.update(f.read().split())
                # with open(config.garage_file,"w") as f:
                    # f.write(" ".join(garage))
                # print("local garage update complete")
                # synchronize_garage()
                # break
            # finally:garage_rlock.release()
        # elif x=="e":
            # break

def synchronize_garage():    #当你使用多台计算机下载图片时，你可能需要将你的garage文件同步到你的服务器上以免重复
    try:
        if not config.syn_enable: return
        private_key = paramiko.RSAKey.from_private_key_file(config.RSAKey_file)
        transport = paramiko.Transport((config.sftp_host,config.sftp_port))
        transport.connect(username=config.sftp_username,pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        remotedir=config.sftp_remotedir
        if "garage" not in sftp.listdir(remotedir):
            sftp.put("garage",remotedir+"garage")

        sftp.get(remotedir+"garage","tmp_garage")
        
        with open("tmp_garage","r") as f:
            garage.update(f.read().split())
        os.remove("tmp_garage")
        
        with open("garage","w") as f:
            f.write(" ".join(garage))
        
        sftp.put("garage",remotedir+"garage")
        
        print("synchronize garage succeeded")
    except Exception as e:
        print("synchronize garage failed")
        print(e)
    finally:
        try:
            transport.close()
        except Exception as e:
            pass

def testrecommen():    #未完成功能
    r=session_requests.get(pixiv_root+"recommended.php")
    tree=html.fromstring(r.text)
    token=tree.xpath("/pixiv.context.token")
    print(token)
    # "//input[@name='post_key']/@value"
        
def complete_urllist(clsf):
    def get_artist_imglist(artistid):
        try:
            url=config.url_artist_all_template%(artistid)
            r=session_requests.get(url)
            js=r.json()
            imglist=list(dict(js['body']['illusts']).keys())+list(dict(js['body']['manga']).keys())
            return imglist
        except Exception as e:
            traceback.print_exc()
            return []        
    def get_artist_artistname(artistid):
        try:
            url=config.url_artist_template%(artistid,1)
            r=session_requests.get(url)
            res=re.search(r'"userId":"\d+","name":"([^"]*)"?',r.text)
            artist_name=res.group(1)
            artist_name=artist_name.encode('utf-8').decode('unicode_escape')
            return artist_name
        except Exception as e:
            traceback.print_exc()
            return "artist_"+artistid
    
    newclsf=[]
    for clsf_name,item_list in clsf:
        if clsf_name=="tag": 
            for tag,pagenum in item_list:newclsf.append(("tag-"+tag,[config.url_tag_template%(tag,p) for p in range(1,pagenum+1)]))
        elif clsf_name=="illustrator":
            for artistname,artistid,pagenum in item_list:
                if artistname=='?':
                    artistname=get_artist_artistname(artistid)
                imglist=get_artist_imglist(artistid)
                newclsf.append(("illustrator-"+artistname,[imglist]))
        elif clsf_name=="bookmark":
            #对于bookmark，后者表示页数
            pagenum=item_list
            newclsf.append(("bookmark",[config.url_bookmark_template%(p) for p in range(1,pagenum+1)]))
        elif clsf_name=="rank_global":
            newclsf.append(("rank_global",[config.url_rank_global_template]))
        elif clsf_name in ["rank_daily","rank_weekly","rank_original","rank_daily_r18","rank_male_r18","rank_weekly_r18"]:
            url_template=getattr(config,"url_"+clsf_name+"_template")
            pagenum=item_list
            newclsf.append((clsf_name,[url_template%(p) for p in range(1,pagenum+1)]))
        else: newclsf.append((clsf_name,item_list))
    return newclsf

    
def get_master_imagelist_from_resp(classi,r):
    def gmifr_tag(r):
        url=r.url
        # url=url.replace("/artworks","")
        url=re.sub(r"/[a-zA-Z]+?(?=\?)","",url,count=1)
        url=url.replace("/tags/","/ajax/search/artworks/")
        ajax=url
        r=session_requests.get(ajax)
        js=r.json()
        popular_permen_list=list(map(lambda x:x['illustId'],js['body']['popular']['permanent']))
        popular_rec_list=list(map(lambda x:x['illustId'],js['body']['popular']['recent']))
        data_list=list(map(lambda x:x['illustId'],js['body']['illustManga']['data']))
        retlist=popular_permen_list+popular_rec_list+data_list
        return retlist

    def gmifr_bookmark(r):
        tree=html.fromstring(r.text)
        res=tree.xpath("//div[@data-items]/@data-items")[0]
        js=json.loads(unescape(res))
        retlist=list(map(lambda x:x['illustId'],js))
        return retlist
    try:
        # print(r.text)
        print(r.url)
        if classi=="tag":
            retlist=gmifr_tag(r)
        elif classi=="bookmark":
            retlist=gmifr_bookmark(r)
        else:
            retlist=re.findall(r'(?<=img-master/img)(.*?)(?=_master)',r.text)
            try:
                retlist_temp=gmifr_tag(r)
                retlist.extend(retlist_temp)
            except Exception as e:
                pass
            try:
                retlist_temp=gmifr_bookmark(r)
                retlist.extend(retlist_temp)
            except Exception as e:
                pass
            retlist=list(set(retlist))         
        return retlist
    except Exception as e:
        traceback.print_exc()
        return []

def check_tempfile_overflow(maxitems):
    if not os.path.exists(config.temp_save_root) : os.makedirs(config.temp_save_root)
    temp_file_list=os.listdir(config.temp_save_root)

    if(len(temp_file_list)>maxitems):
        for filename in temp_file_list:os.remove(config.temp_save_root+filename)
        print("cleared config.temp_save_root")
    
        
def random_one_by_classfi(classi,label="fate"):
    '''classi= "normalrank" or "tag" or "r18rank" '''
    try:
        if classi=="tag" and "r-18" not in label.lower():label+=" -r-18"
        
        check_tempfile_overflow(config.max_tempfile_number)
        if not os.path.exists(config.local_save_root) : os.makedirs(config.local_save_root)
        
        if classi.lower()=="normalrank":classification=[("normalRank",[pixiv_root+"ranking.php?mode=daily&p=1",pixiv_root+"ranking.php?mode=daily&p=2",pixiv_root+"ranking.php?mode=original"])]
        elif classi.lower()=="tag":classification=complete_urllist([("tag",[(label,5)])])
        elif classi.lower()=="r18rank":classification=complete_urllist([("r18Rank",[pixiv_root+"ranking.php?mode=daily_r18&p=1",pixiv_root+"ranking.php?mode=male_r18&p=1",pixiv_root+"ranking.php?mode=weekly_r18&p=1",pixiv_root+"ranking.php?mode=weekly_r18&p=2"])])
        else: return None
        
        try: login()
        except Exception as e:print(e);print('Connect failed');return None
        
        url=random.choice(classification[0][1])
        r=session_requests.get(url)
        #imagelist=re.findall(r'(?<=img-master/img)(.*?)(?=_master)',r.text)
        imagelist=get_master_imagelist_from_resp(classi.lower(),r)
        if (not imagelist) and classi.lower()=='tag':
            url=random.choice(complete_urllist([("tag",[(label,1)])])[0][1])
            r=session_requests.get(url)
            imagelist=get_master_imagelist_from_resp(classi.lower(),r)
            if r.status_code!=200 or not imagelist:return None    
        img=random.choice(imagelist)
        imgid=re.search('\d+(?=(_|$))',img).group(0)
        toDownlist=imgid2source_url(imgid,"single",config.local_save_root)
        if len(toDownlist)>0: orgurl,filename=toDownlist[0]
        else :return None
        if os.path.exists(filename): return filename
        refer=referpfx+imgid
        imgidext=os.path.splitext(os.path.basename(filename))[0]
        # print(orgurl,filename,refer,imgid,imgidext)
        # exit(0)
        if downloadImage(orgurl,filename,header={"referer":refer},imgid=imgid,imgidext=imgidext):
            return filename
        else:
            return None
    except Exception as e:
        traceback.print_exc()

def imgid2source_url(imgid,mode="single",local_save=None):
    if not local_save:local_save=config.local_save_root
    refer=referpfx+imgid
    try:
        toDownlist=[]
        r=session_requests.get(refer,timeout=25)
        tree=html.fromstring(r.text)
        content=tree.xpath("/html/head/meta[@id='meta-preload-data']/@content")[0]
        jsdata=content
        if jsdata:js=json.loads(jsdata)
        else:
            print("load jsdata fail")
            return []
        js=js["illust"][imgid]
        pageCount=js["pageCount"]
        match_manga=pageCount>1
        original_url=js['urls']['original']
        if mode=="single":
            toDownlist.append((original_url,local_save+os.path.split(original_url)[1]))
        else:
            for i in range(0,pageCount):
                original_url_p=original_url.replace("p0","p"+str(i))
                toDownlist.append((original_url_p,local_save+os.path.split(original_url_p)[1]))
        return toDownlist
    except Exception as e:
        faillog.append(imgid)
        print(e)
        return []

def load_config():
    global proxies
    
    if config.proxies_enable:
        proxies={'http': config.socks,'https': config.socks}
    else:
        proxies=None
    
    for ch in ['%y','%m','%d','%H','%M','%S']:
        config.local_save_root=config.local_save_root.replace(ch,datetime.datetime.now().strftime(ch))

    
    # classi_list=['normalRank','r18Rank','bookmark','tag','illustrator']
    #classification=[]
    # for classi in classi_list:
        # if config.getboolean('classification',classi):
            # classification.append((classi,eval(config['classification'][classi+'_list'])))

    
#----------Constants
pixiv_root="https://www.pixiv.net/"
referpfx=r'https://www.pixiv.net/member_illust.php?mode=medium&illust_id='



#----------global vars
load_config()
if config.syn_enable: import paramiko
session_requests=requests.session()
session_requests.proxies=proxies
write_rlock=threading.RLock()
garage_rlock=threading.RLock()
garage=set()
faillog=[]



def batch_download(classification,max_pic_num=100,deep_into_manga=False,add_classname_in_path=True):
    global listen_active
    #----------PREDO
    
    #尝试登陆, 登陆分离
    # try: login()
    # except Exception as e:print(e);print('Connect failed');traceback.print_exc();exit(0)
    #创建存储位置
    if not os.path.exists(config.local_save_root) : os.makedirs(config.local_save_root)
    #检查garage文件并更新garage
    if os.path.exists(config.garage_file) : #garage文档存放车库清单，避免文件重复
        with open(config.garage_file,"r") as f:
            garage.update(f.read().split())
    
    classification=complete_urllist(classification)
    # exit(0)
    #synchronize_garage()

    pic_num=0
    # faillog=[]
    threads=[]
    # write_rlock=threading.RLock()
    # garage_rlock=threading.RLock()
    #----------MAINPROC
    #listen_active=True
    # t=threading.Thread(target=listener)
    # t.start()
    for classi,urlList in classification:
        local_save=config.local_save_root+(classi+"/" if add_classname_in_path else "")
        if not os.path.exists(local_save) : os.makedirs(local_save)
        classi_mode="tag" if "tag" in classi else "illustrator" if "illustrator" in classi else classi
        for pageUrl in urlList:    
            try:
                if classi_mode=="illustrator":
                    imagelist=pageUrl
                else:
                    rankPage=session_requests.get(pageUrl)
                    imagelist=get_master_imagelist_from_resp(classi_mode,rankPage)
            except Exception as e:
                faillog.append(pageUrl+"Pagefail")
                continue
            for img in imagelist:
                try:
                    imgid=re.search('\d+(?=(_|$))',img).group(0)
                except Exception as e:
                    print('fail : '+img)
                    faillog.append(img)
                    continue
                refer=referpfx+imgid
                #在非manga模式的情况下提前剪枝
                if(not deep_into_manga and imgid+"_p0" in garage):
                    print("Skipped %s"%imgid)
                    continue            
                toDownlist=imgid2source_url(imgid,"manga" if deep_into_manga else "single",local_save)
                for orgurl,filename in toDownlist:
                    imgidext=os.path.splitext(os.path.basename(filename))[0]
                    if (imgidext in garage) and not ("illustrator"==classi_mode):
                        print("Skipped %s"%imgid)
                        continue
                    if os.path.exists(filename):
                        print("image file %s existed"%imgid)
                        garage.add(imgidext)
                        continue
                    print("<"+orgurl+">")            
                    t=threading.Thread(target=downloadImage,args=(orgurl,filename),kwargs={"header":{"referer":refer},"imgid":imgid,"imgidext":imgidext})
                    threads.append(t)
                    while sum(map(lambda x:1 if x.is_alive() else 0,threads))>=config.max_thread_num : time.sleep(1)
                    t.start()
                    
                    #控制数量 提前结束
                    pic_num+=1
                    if max_pic_num!=-1 and pic_num>=max_pic_num:
                        for t in threads :
                            if t.is_alive():t.join()
                        if faillog:
                            print('-------------------------faillog-------------------------')
                            for log in faillog:print(log)
                        return

        for t in threads :
            if t.is_alive():t.join()

    #_______________AFTER
    if faillog:
        print('-------------------------faillog-------------------------')
        for log in faillog:print(log)

    # with open(config.garage_file,"w") as f:
        # f.write(" ".join(garage))
        
    #synchronize_garage()


    #listen_active=False
    #print("END")
    
#FUNCTIONS
def set_value(value_name,value):
    '''Legal attributes:
        username
        password
        local_save_root
        garage_file
        cookies_file
        max_thread_num
        socks: set None if not use
    '''

    if value_name not in ['username','password','local_save_root','garage_file','cookies_file','max_thread_num','socks','phantomjs','firefox','chrome']:
        raise ValueError("Illegal Attribute")
    if value_name=="socks":
        if not value:
            config.proxies_enable=False
            session_requests.proxies=None
        else:
            value=value.replace("socks5h://","")
            setattr(config,value_name,"socks5h://"+value)
            config.proxies_enable=True
            proxies={'http': config.socks,'https': config.socks}
            session_requests.proxies=proxies
    elif value_name=="local_save_root":
        if value[-1]!='/':value=value+"/"
        for ch in ['%y','%m','%d','%H','%M','%S']:
            if ch in value: value=value.replace(ch,datetime.datetime.now().strftime(ch))
        setattr(config,value_name,value)
    else:
        setattr(config,value_name,value)
        
def get_value(value_name):
    '''Legal attributes:
        username
        password
        local_save_root
        garage_file
        cookies_file
        max_thread_num
        socks: set None if not use
    '''
    if value_name not in ['username','password','local_save_root','garage_file','cookies_file','max_thread_num','socks','phantomjs','firefox','chrome']:
        return None
    return getattr(config,value_name)
    
def save_garage(garage_file = None):
    '''Save downloaded image list, to avoid repeating downloading'''
    if not garage_file:
        garage_file=config.garage_file
    with open(garage_file,"w") as f:
        f.write(" ".join(garage))

def dl_tag(tag,pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"tag")
    classification=[("tag",[(tag,(pic_num+ppp-1)//ppp)])]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)

def dl_artist(artist_id,pic_num,deep_into_manga=True,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"illustrator")
    classification=[("illustrator",[("?",artist_id,-1 if pic_num==-1 else ((pic_num+ppp-1)//ppp))])]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)

def dl_bookmark(pic_num,deep_into_manga=True,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"bookmark")
    classification=[("bookmark",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_rank_global(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_global")
    classification=[("rank_global",1)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_rank_daily(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_daily")
    classification=[("rank_daily",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_rank_weekly(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_weekly")
    classification=[("rank_weekly",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)

def dl_rank_original(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_original")
    classification=[("rank_original",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)

def dl_rank_daily_r18(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_daily_r18")
    classification=[("rank_daily_r18",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_rank_male_r18(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_male_r18")
    classification=[("rank_male_r18",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_rank_weekly_r18(pic_num,deep_into_manga=False,add_classname_in_path=True):
    ppp=getattr(config,"pic_per_page_"+"rank_weekly_r18")
    classification=[("rank_daily",(pic_num+ppp-1)//ppp)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
def dl_diy_urls(urls,pic_num,deep_into_manga=False,add_classname_in_path=True):
    if not isinstance(urls,list):
        urls=[urls]
    classification=[("DIY_urls",urls)]
    batch_download(classification,pic_num,deep_into_manga,add_classname_in_path)
    
if __name__=="__main__":
    # batch_download()
    print(random_one_by_classfi("tag","azurlane"))
    # login()
    # print(get_artist_artistname("21848"))

