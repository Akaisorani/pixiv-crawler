# pixiv-crawler
pixiv image crawler

## functions

Download image by
* ranklist such as dailyrank
* tags
* illustrator's illustration list

or random a image by
* ranklist
* tags

## features

* it can download images by **_8 threads_**(the maxnumber of threads can be adjusted) to accelerate the progress
* in most case it download the first picture of a **_manga_** type illustration, but in the illustrator's illustration list it will download the **_full manga_**(of course you can adjust the condition to decide when to download full)
* it can **_login_** with your account automatically with your account name and password
* after once login it will save **_cookies_** to local to avoid login each time
* it can save a **_garage file_** as a list of the image id you have downloaded to avoid download images repeatedly(because some ranklist doesn't change a lot next day)
* it can also **_synchronize_** your garage file with your remote server(if you have) to make sure not download repeatedly on your different computers
* for illustrator's illustration list, **_artist id_** must be provided, if set artist name as "?" then it will be found on the website, if set download page number as -1, then it will download all pages from this artist.
* for some reasons, you know, it need **_proxies_** to visit pixiv.net in some area, so you can set proxies in the config.properties.
* **_config.properties_** contains most configs so you needn't to edit the code source file.
