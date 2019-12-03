# pixiv-crawler
pixiv image crawler

Github [https://github.com/Akaisorani/pixiv-crawler](https://github.com/Akaisorani/pixiv-crawler)
## How to install

```
pip install pixiv_crawler
```

To pass the captcha in login, we use selenium+phantomjs. So you need to install selenium and phantomjs (or chrome/firefox with headless model).

## Functions

Download image by
* ranklist such as dailyrank
* tags
* illustrator's illustration list
* your bookmark list
* DIY urls

or random a image by
* ranklist
* tags

## How to use

### Example

```
import pixiv_crawler as pc

pc.set_value('username','your account name')
pc.set_value('password','your account password')
# pc.set_value('socks','127.0.0.1:8388')
# pc.set_value("local_save_root","./%y.%m.%d")
# pc.set_value("cookies_file","./cookies.txt")
# pc.set_value("garage_file","./garage.txt")
pc.set_value("phantomjs","/usr/local/bin/phantomjs") # for simulating log in process. the path will be (bala...)/phantomjs.exe on Windows
pc.login()

pc.dl_rank_daily(20)
pc.dl_bookmark(20)
pc.dl_artist(4187518,pic_num=-1,deep_into_manga=False)
pc.dl_tag('azur lane',20)
pc.dl_diy_urls(['https://www.pixiv.net/ranking.php?mode=weekly'],20)
```

## ~~Features~~

* it can download images by **_8 threads_**(the maxnumber of threads can be adjusted) to accelerate the progress
* in most case it download the first picture of a **_manga_** type illustration, but in the illustrator's illustration list it will download the **_full manga_**(of course you can adjust the condition to decide when to download full)
* it can **_login_** with your account automatically with your account name and password
* after once login it will save **_cookies_** to local to avoid login each time
* it can save a **_garage file_** as a list of the image id you have downloaded to avoid download images repeatedly(because some ranklist doesn't change a lot next day)
* it can also **_synchronize_** your garage file with your remote server(if you have) to make sure not download repeatedly on your different computers
* for illustrator's illustration list, **_artist id_** must be provided, if set artist name as "?" then it will be found on the website, if set download page number as -1, then it will download all pages from this artist.
* for some reasons, you know, it need **_proxies_** to visit pixiv.net in some area, so you can set proxies in the config.properties.
* **_config.properties_** contains most configs so you needn't to edit the code source file.

## Function List
```
login (save_cookies=True)
set_value (value_name,value)
get_value (value_name,value)
save_garage (garage_file = None)
dl_tag (tag,pic_num,deep_into_manga=False,add_classname_in_path=True)
dl_artist (artist_id,pic_num,deep_into_manga=True,add_classname_in_path=True)
dl_bookmark (pic_num,deep_into_manga=True,add_classname_in_path=True)
dl_rank_global (pic_num,deep_into_manga=False,add_classname_in_path=True)
dl_rank_daily (pic_num,deep_into_manga=False,add_classname_in_path=True)
dl_rank_weekly (pic_num,deep_into_manga=False,add_classname_in_path=True)
dl_rank_original (pic_num,deep_into_manga=False,add_classname_in_path=True)
...
dl_diy_urls (urls,pic_num,deep_into_manga=False,add_classname_in_path=True)
random_one_by_classfi (classi,label="")
```

## Attribute List
```
username
password
local_save_root
garage_file
cookies_file
max_thread_num
socks: set None if not use
phantomjs
firefox
chrome
```
