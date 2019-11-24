# coding: utf-8
["DEFAULT"]
max_tempfile_number = 100
max_thread_num = 8

["account"]
username = ""
password = ""

["proxies"]
proxies_enable = False
socks = ""

["path"]
local_save_root = "./default_save/"
temp_save_root = "./temp_save/"

["data"]
garage_file = "./garage.txt"
cookies_file = "./cookies.txt"

["classification"]
pic_per_page_tag=40
pic_per_page_illustrator=48
pic_per_page_bookmark=20
pic_per_page_rank_global=100
pic_per_page_rank_daily=50
pic_per_page_rank_weekly=50
pic_per_page_rank_original=50
pic_per_page_rank_daily_r18=50
pic_per_page_rank_male_r18=50
pic_per_page_rank_weekly_r18=50
# normalRank = True
# r18Rank = False
# bookmark = False
# tag = False
# illustrator = False

# [("tag",page number), ...]
tag_list = []

# [("illustrator name", "illustrator id", page number), ...]
# "illustrator name" as "?" means find it on the website.
# page number as -1 means all pages of the illustrator
# "illustrator id" is essential
illustrator_list = []

# a page normally contains 20 pictures
bookmark_list = 0

pixiv_root="https://www.pixiv.net/"

# url_tag_template=pixiv_root+"search.php?word=%s&order=date_d&p=%d"
url_tag_template=pixiv_root+"tags/%s/artworks?p=%d"
url_artist_template=pixiv_root+"member_illust.php?id=%s&type=all&p=%d"
url_artist_all_template=pixiv_root+"ajax/user/%s/profile/all"
url_bookmark_template=pixiv_root+"bookmark_new_illust.php?p=%d"
# rank_global_list=1
url_rank_global_template=pixiv_root+"ranking_area.php?type=detail&no=6"
# rank_daily_list= page_number
url_rank_daily_template=pixiv_root+"ranking.php?mode=daily&p=%d"
url_rank_weekly_template=pixiv_root+"ranking.php?mode=weekly&p=%d"
url_rank_original_template=pixiv_root+"ranking.php?mode=original&p=%d"
url_rank_daily_r18_template=pixiv_root+"ranking.php?mode=daily_r18&p=%d"
url_rank_male_r18_template=pixiv_root+"ranking.php?mode=male_r18&p=%d"
url_rank_weekly_r18_template=pixiv_root+"ranking.php?mode=weekly_r18&p=%d"
 
["syn"]
syn_enable = False
RSAKey_file = ""
sftp_host = ""
sftp_port = 22
sftp_username = ""
sftp_remotedir = ""

["browser"]
phantomjs = ""
firefox=""
chrome=""
