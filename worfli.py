import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import unicodedata

##### 変更箇所 #####
REFRESH_INTERVAL_SEC=1.5          # 更新間隔
QUESTNAME_PADDING_LENGTH=22     # クエスト名の空白埋め個数　長くなったら増やしてください（全角=2,半角=1）
###################


def fetch_quest_list():
    r=requests.get("https://appmedia.jp/worldflipper/4181962")
    soup=BeautifulSoup(r.content,"html.parser")
    quest_list=soup.find("div",{"id":"frm_wrapper"}).find_all("option")
    quest_list=[v.text for v in quest_list]
    return quest_list

def padding(text,num=6):
    text_counter = 0
    for c in text:
        j = unicodedata.east_asian_width(c)
        if "F"==j or "W"==j or "A"==j:
            text_counter = text_counter + 2
        else:
            text_counter = text_counter + 1
    return str(text)+" "*(num-text_counter)
def main():
    quest_list=fetch_quest_list()
    print("表示モードを選んでください\n  1: すべて\n  2: 絞り込み")
    mode=input("モード: ")
    if mode=="2":
        print("\nクエストを選んでください (カンマ区切りで複数選択可)")
        for i,quest in enumerate(quest_list):
            print("  {0}: {1}".format(i,quest))
        questnum_list=[int(i) for i in input("クエスト番号：").split(",")]
        quest_list=[quest_list[i] for i in questnum_list]
    last_postnum=0
    is_new_recuruits=False
    sleep(REFRESH_INTERVAL_SEC)
    zenhan=lambda text:text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    print("-----")
    while 1:
        r=requests.get("https://appmedia.jp/worldflipper/4181962")
        soup=BeautifulSoup(r.content,"html.parser")
        recuruit_list=soup.findAll("div",{"class":"comments_main_div"})
        for recuruit in reversed(recuruit_list):
            postnum=int(recuruit.find("div",{"class":"comments_title_div"}).p.span.text)
            if last_postnum<postnum:
                questname=recuruit.find("div",{"class":"world_flipper_quest_nm_lb"}).text[6:]
                if not questname in quest_list:
                    continue
                roomid=zenhan(recuruit.find("div",{"class":"world_flipper_comment_lb"}).text)
                freespace=recuruit.find("span",{"id":"result_comment"}).text
                print(roomid[:3],roomid[3:],end=" | ")
                print(padding(questname,QUESTNAME_PADDING_LENGTH),end=" | ")
                print(freespace.replace("\n"," "))
                last_postnum=postnum
                is_new_recuruits=True
        if is_new_recuruits:
            print("-----",datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        is_new_recuruits=False
        sleep(REFRESH_INTERVAL_SEC)
main()
