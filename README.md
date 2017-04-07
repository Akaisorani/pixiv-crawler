# pixiv-crawler
pixiv image crawler

## functions

Download image from
* images listed in ranklist such as dailyrank
* provided tags
* illustrator's illustration list

## features

* it can download images by **_8 threads_**(the maxnumber of threads can be adjusted) to accelerate the progress
* in most case it download the first picture of a **_manga_** type illustration, but in the illustrator's illustration list it will download the **_full manga_**(of course you can adjust the condition)
* it can **_login_** with your account automatically with your account name and password
* after once login it will save **_cookies_** to local to avoid login each time
* it can save a **_garage file_** as a list of the image id you have downloaded to avoid download images repeatedly(because some ranklist doesn't change a lot next day)
* it can also **_synchronize_** your garage file with your remote server(if you have) to make sure not download repeatedly on your different computers
