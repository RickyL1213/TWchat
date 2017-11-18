# -*- coding: UTF-8
import os
import gui as wegui
from itchat.content import *
import itchat
 
def get_contact_name(msg):
    return msg['User']['RemarkName'] if msg['User']['RemarkName'] else msg['User']['NickName']
def get_group_name(msg):
    group_name=""
    print(msg)
    if not msg['User']['NickName']:
        for member in msg['User']['MemberList']:
            group_name+=member['NickName']
    else:
        group_name=msg['User']['NickName']
    if len(group_name)>15:
        return u"群聊: "+group_name[:12]+"..."
    else:
        return u"群聊: "+group_name
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
def start():
    @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO,FRIENDS])
    def recive_contact_msg(msg):
        contact_name = get_contact_name(msg)
        notify('TWchat',"new message from: "+contact_name)
        if msg.type is not 'Text':
            msg['Text']=str(msg.type)+" is not supported yet please check this on your phone"
        wechatMain.recive_message(msg,contact_name)
    
    @itchat.msg_register(TEXT, isGroupChat=True)
    def recive_group_msg(msg):
        group_name = get_group_name(msg)
        notify('TWchat',"new message from: "+group_name)
        wechatMain.recive_message(msg,group_name)
        return   
    def on_contact_item_click(button,info):
        wechatMain.chatListBox.addNewChat(info[0],info[1])
        wechatMain.set_current_chat(info[0],info[1])
        wechatMain.chatListBox.show_chat()
        return 
    def on_chat_item_click(button,info):
        wechatMain.set_current_chat(info[0],info[1])
        return
    palette = [
        ('left', 'black', 'light gray'),
        ('right', 'black', 'dark cyan'),
        ('button', 'dark green','black'),
        ('mybg', 'black','dark cyan'),
        ('tobg', 'dark blue','light gray'),
        ('edit', 'dark cyan','black'),
        ('bg', 'dark green', 'black'),]
    print ('''
 _____  _    _  _____  _   _   ___   _____ 
|_   _|| |  | |/  __ \| | | | / _ \ |_   _|
  | |  | |  | || /  \/| |_| |/ /_\ \  | |  
  | |  | |/\| || |    |  _  ||  _  |  | |  
  | |  \  /\  /| \__/\| | | || | | |  | |  
  \_/   \/  \/  \____/\_| |_/\_| |_/  \_/  
            ''')

    wechatMain = wegui.WechatMain(palette)
    itchat.auto_login(enableCmdQR=2,hotReload=True)
    itchat.run(blockThread=False)
    userInfo =itchat.web_init()['User']
    owner_id = userInfo['UserName']
    owner_name = userInfo['NickName']
    contactlist= itchat.get_friends(update=True)
    chatlist = itchat.get_chatrooms()
    contactlist = sorted(contactlist,key=lambda x:(x['RemarkPYInitial'],x['PYInitial']))
    wechatMain.initUserInfo(owner_id,owner_name,on_contact_item_click,on_chat_item_click,contactlist,chatlist)
    wechatMain.bind_itchat(itchat)
    wechatMain.createLoop()

if __name__ == '__main__':
    start()