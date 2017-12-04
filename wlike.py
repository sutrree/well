# -*- coding: utf-8 -*-

import treetc
from treetc.lib.curve.ttypes import *
from datetime import datetime
import time,random,sys,json,codecs,threading,glob,re,base64

cl = treetc.LINE()
print u"login start"
cl.login(qr=True)
cl.loginResult()
ks = ki = kk = kc = cl 
print u"login success"
reload(sys)
sys.setdefaultencoding('utf-8')
i = 0
print u"login success"

KAC=[cl,ki,kk,kc,ks]
mid = cl.getProfile().mid
Amid = ki.getProfile().mid
Bmid = kk.getProfile().mid
Cmid = kc.getProfile().mid
Dmid = ks.getProfile().mid

Bots=[mid,Amid,Bmid,Cmid,Dmid]
admin=["ucd886b532f581aa4de98af5898719392"]
wait = {
    'protect':False,
    'protectinv':False,
    'protectqr':False,	
    'contact':True,
    'autoJoin':True,
    'autoCancel':{"on":True,"members":10},
    'leaveRoom':True,
    'timeline':True,
    'autoAdd':True,
    'message':"Thanks for add me",
    "lang":"JP",
    "comment":"Auto Like",
    "commentOn":True,
    "likeOn":True,
    "commentBlack":{},
    "wblack":False,
    "dblack":False,
    "clock":False,
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False,
    "protectionOn":False,
    "atjointicket":False
    }

wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
    }

cancelinvite = {
    'autoCancel':True
}

setTime = {}
setTime = wait2['setTime']
#-------------------------------------------------------------------------# 
def mention(to, nama):
    aa = ""
    bb = ""
    strt = int(14)
    akh = int(14)
    nm = nama
    for mm in nm:
      akh = akh + 2
      aa += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(mm)+"},"""
      strt = strt + 6
      akh = akh + 4
      bb += "\xe2\x95\xa0 @x \n"
    aa = (aa[:int(len(aa)-1)])
    msg = Message()
    msg.to = to
    msg.text = "\xe2\x95\x94\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\n"+bb+"\xe2\x95\x9a\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90\xe2\x95\x90"
    msg.contentMetadata ={'MENTION':'{"MENTIONEES":['+aa+']}','EMTVER':'4'}
    print "[Command] Tag All"
    try:
       cl.sendMessage(msg)
    except Exception as error:
       print error
#-------------------------------------------------------------------------#   
def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
#-------------------------------------------------------------------------#   
def autolike():
    count = 1
    while True:
        try:
           for posts in cl.activity(1)["result"]["posts"]:
             if posts["postInfo"]["liked"] is False:
                if wait["likeOn"] == True:
                   cl.like(posts["userInfo"]["writerMid"], posts["postInfo"]["postId"], 1001)
                   print "Like"
                   if wait["commentOn"] == True:
                      if posts["userInfo"]["writerMid"] in wait["commentBlack"]:
                         pass
                      else:
                          cl.comment(posts["userInfo"]["writerMid"],posts["postInfo"]["postId"],wait["comment"])
        except:
            count += 1
            if(count == 50):
                sys.exit(0)
            else:
                pass
thread2 = threading.Thread(target=autolike)
thread2.daemon = True
thread2.start()
#-------------------------------------------------------------------------# 
def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if wait["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                if (wait["message"] in [""," ","\n",None]):
                    pass
                else:
                    cl.sendText(op.param1,str(wait["message"]))						
        if op.type == 13:
            if mid in op.param3:
                G = cl.getGroup(op.param1)
                if wait["autoJoin"] == True:
                    if wait["autoCancel"]["on"] == True:
                        if len(G.members) <= wait["autoCancel"]["members"]:
                            cl.rejectGroupInvitation(op.param1)
                        else:
                            cl.acceptGroupInvitation(op.param1)
                    else:
                        cl.acceptGroupInvitation(op.param1)
                elif wait["autoCancel"]["on"] == True:
                    if len(G.members) <= wait["autoCancel"]["members"]:
                        cl.rejectGroupInvitation(op.param1)             
#-------------------------------------------------------------------------# 
        if op.type == 13:
            if op.param2 not in Bots:
                if op.param2 in Bots:
                    pass
            elif wait["inviteprotect"] == True:
                cl.cancelGroupInvitation(op.param1,[op.param3])
                if op.param2 not in Bots:
                    if op.param2 in Bots:
                        pass
                    elif wait["cancelprotect"] == True:
                        cl.cancelGroupInvitation(op.param1,[contact.mid for contact in cl.getGroup(op.param1).invitee])
        if op.type == 22:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
        if op.type == 24:
            if wait["leaveRoom"] == True:
                cl.leaveRoom(op.param1)
#-------------------------------------------------------------------------# 

            elif msg.text in ["Gift","gift"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': '3b92ccf5-54d3-4765-848f-c9ffdc1da020',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '3'}
                msg.text = None
                cl.sendMessage(msg)
																	
#-------------------------------------------------------------------------#								
            elif msg.text in ["Cancel","cancel"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    if group.invitee is not None:
                        gInviMids = [contact.mid for contact in group.invitee]
                        cl.cancelGroupInvitation(msg.to, gInviMids)
                    else:
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,"No one is inviting。")
                        else:
                            cl.sendText(msg.to,"Sorry, nobody absent。")
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can not be used outside the group。")
                    else:
                        cl.sendText(msg.to,"Not for use less than group")

#-------------------------------------------------------------------------#
        if op.type == 25:
            msg = op.message
            if msg.text in ["Speed","speed","Sp","sp"]:
                    start = time.time()
                    elapsed_time = time.time() - start
                    cl.sendText(msg.to, "%sseconds" % (elapsed_time))
#-------------------------------------------------------------------------#											
            if msg.text == "Ginfo":
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "close"
                        else:
                            u = "open"
                        cl.sendText(msg.to,"[Group Name]\n" + str(ginfo.name) + "\n[Group ID]\n" + msg.to + "\n[Group Maker]\n" + gCreator + "\n[Status Profil]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\nNumber of Members : " + str(len(ginfo.members)) + "Member\nMember Pending : " + sinvitee + "Member\nQR Link :" + u + " ")
                    else:
                        cl.sendText(msg.to,"[Group Name]\n" + str(ginfo.name) + "\n[Group ID]\n" + msg.to + "\n[Group Maker]\n" + gCreator + "\n[Status Profil]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can not Be Used Outside of Group")
                    else:
                        cl.sendText(msg.to,"Can not Be Used Outside of Group")
#-------------------------------------------------------------------------#													
            elif "Gcreator" == msg.text:
              if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    cl.sendText(msg.to, "Group Creator : " + gCreator)
#-------------------------------------------------------------------------#	
            elif msg.text in ["Gcreator:inv"]:
              if msg.toType == 2:
                 ginfo = cl.getGroup(msg.to)
                 gCreator = ginfo.creator.mid
                 try:
                    cl.findAndAddContactsByMid(gCreator)
                    cl.inviteIntoGroup(msg.to,[gCreator])
                    print "Successfully Invite Group Creator"
                 except:
                    pass

#----------------------------- TAG ALL MEMBER -------------------------------#
            if msg.text.lower() in ["tagall"]:
                group = cl.getGroup(msg.to)
                nama = [contact.mid for contact in group.members]
                nm1, nm2, nm3, nm4, nm5, jml = [], [], [], [], [], len(nama)
                if jml <= 100:
                    mention(msg.to, nama)
                    if jml > 100 and jml < 200:
                        for i in range(0, 100):
                            nm1 += [nama[i]]
                    mention(msg.to, nm1)
                    for j in range(101, len(nama)):
                        nm2 += [nama[j]]
                    mention(msg.to, nm2)
                if jml > 200 and jml < 300:
                    for i in range(0, 100):
                        nm1 += [nama[i]]
                    mention(msg.to, nm1)
                    for j in range(101, 200):
                        nm2 += [nama[j]]
                    mention(msg.to, nm2)
                    for k in range(201, len(nama)):
                        nm3 += [nama[k]]
                    mention(msg.to, nm3)
                if jml > 300 and jml < 400:
                    for i in range(0, 100):
                        nm1 += [nama[i]]
                    mention(msg.to, nm1)
                    for j in range(101, 200):
                        nm2 += [nama[j]]
                    mention(msg.to, nm2)
                    for k in range(201, 300):
                        nm3 += [nama[k]]
                    mention(msg.to, nm3)
                    for l in range(301, len(nama)):
                        nm4 += [nama[l]]
                    mention(msg.to, nm4)
                if jml > 400 and jml < 500:
                    for i in range(0, 100):
                        nm1 += [nama[i]]
                    mention(msg.to, nm1)
                    for j in range(101, 200):
                        nm2 += [nama[j]]
                    mention(msg.to, nm2)
                    for k in range(201, 300):
                        nm3 += [nama[k]]
                    mention(msg.to, nm3)
                    for l in range(301, 400):
                        nm4 += [nama[l]]
                    mention(msg.to, nm4)
                    for h in range(401, len(nama)):
                        nm5 += [nama[h]]
                    mention(msg.to, nm5)
                if jml > 500:
                    cl.sendText(msg.to,'Member over limit.')
                cnt = Message()
                cnt.text = "Done : " + str(jml) +  " Members"
                cnt.to = msg.to
                cl.sendMessage(cnt)
#-------------------------------------------------------------------------#	
            elif msg.text in ["Add:on"]:
                if wait["autoAdd"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on。")
                    else:
                        cl.sendText(msg.to,"done。")
                else:
                    wait["autoAdd"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"done。")
                    else:
                        cl.sendText(msg.to,"To be open.")
            elif msg.text in ["Add:off"]:
                if wait["autoAdd"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on。")
                    else:
                        cl.sendText(msg.to,"done。")
                else:
                    wait["autoAdd"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"done。")
                    else:
                        cl.sendText(msg.to,"To be off.")
            elif "Massage change:" in msg.text:
                wait["message"] = msg.text.replace("Massage change:","")
                cl.sendText(msg.to,"The message was changed。")
            elif "Massage add:" in msg.text:
                wait["message"] = msg.text.replace("Massage add:","")
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"done。")
                else:
                    cl.sendText(msg.to,"Changed the information.")
            elif msg.text in ["Check add","Automatically add greeting confirmation"]:
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"It is Massage auto add:" + wait["message"])
                else:
                    cl.sendText(msg.to,"Auto-append information is set as follows.\n\n" + wait["message"])
            elif msg.text in ["Language change","Speech change"]:
                if wait["lang"] =="JP":
                    wait["lang"] = "TW"
                    cl.sendText(msg.to,"I changed the language to Chinese.")
                else:
                    wait["lang"] = "JP"
                    cl.sendText(msg.to,"I changed the language to Japanese.")
            elif "Comment set: " in msg.text:
                c = msg.text.replace("Comment set: ","")
                if c in [""," ","\n",None]:
                    cl.sendText(msg.to,"It is a string that can not be changed👈")
                else:
                    wait["comment"] = c
                    cl.sendText(msg.to,"This has been changed👈\n\n" + c)
            elif msg.text in ["Com:on","com:on","Comment:on"]:
                if wait["commentOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"It is already turned on👈")
                    else:
                        cl.sendText(msg.to,"To open👈")
                else:
                    wait["commentOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"It is already turned on")
                    else:
                        cl.sendText(msg.to,"è¦äº†å¼€👈")
            elif msg.text in ["Com:off","com:off","Comment:off"]:
                if wait["commentOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"It is already turned off")
                    else:
                        cl.sendText(msg.to,"It is already turned off")
                else:
                    wait["commentOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Off👈")
                    else:
                        cl.sendText(msg.to,"To turn off") 
            elif msg.text in ["Com","Comment check"]:
                cl.sendText(msg.to,"Auto commenting is\n\n。" + str(wait["comment"]))
								
								
            elif msg.text in ["Contact:on"]:
                if wait["contact"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"contact on already")
                    else:
                        cl.sendText(msg.to,"already on❗")
                else:
                    wait["contact"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on")
                    else:
                        cl.sendText(msg.to,"done..")
            elif msg.text in ["Contact:off"]:
                if wait["contact"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"contact off already")
                    else:
                        cl.sendText(msg.to,"already off。")
                else:
                    wait["contact"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"contact off already")
                    else:
                        cl.sendText(msg.to,"already off")
												
            elif msg.text in ["自動参加:オン","Join:on"]:
                if wait["autoJoin"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on")
                    else:
                        cl.sendText(msg.to,"done")
                else:
                    wait["autoJoin"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on")
                    else:
                        cl.sendText(msg.to,"done")
            elif msg.text in ["Join:off"]:
                if wait["autoJoin"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already off")
                    else:
                        cl.sendText(msg.to,"done")
                else:
                    wait["autoJoin"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already off")
                    else:
                        cl.sendText(msg.to,"done")

            elif msg.text in ["Leave:on","Auto leave:on"]:
                if wait["leaveRoom"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already on")
                    else:
                        cl.sendText(msg.to,"done")
                else:
                    wait["leaveRoom"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"done")
                    else:
                        cl.sendText(msg.to,"è¦äº†å¼€ã€‚")
												
            elif msg.text in ["Leave:off","Auto leave:off"]:
                if wait["leaveRoom"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"already off")
                    else:
                        cl.sendText(msg.to,"done")
                else:
                    wait["leaveRoom"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"done")
                    else:
                        cl.sendText(msg.to,"already")
												
            elif msg.text in ["Cancel:off","cancel:off"]:
                if msg.from_ in admin:
                    if cancelinvite["autoCancel"] == True:
                        cancelinvite["autoCancel"] = False
                        cl.sendText(msg.to, "Auto Cancel turned off")
                        print "[Command]Cancel off executed"
                    else:
                        cl.sendText(msg.to, "Auto Cancel already turned off")
                        print "[Command]Cancel off executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Staff or higher permission required.")
                    print "[Error]Command denied - staff or higher permission required"

            elif msg.text in ["Cancel:on","cancel:on"]:
                if msg.from_ in admin:
                    if cancelinvite["autoCancel"] == False:
                        cancelinvite["autoCancel"] = True
                        cl.sendText(msg.to, "Auto Cancel turned on")
                        print "[Command]Cancel on executed"
                    else:
                        cl.sendText(msg.to, "Auto Cancel already turned on")
                        print "[Command]Cancel on executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Staff or higher permission required.")
                    print "[Error]Command denied - staff or higher permission required"

            elif msg.text in ["Mid","mid","MID"]:
                print "SHOW MID USER"
                cl.sendText(msg.to, msg.from_)
								
            elif msg.text in ["Set"]:
                md = ""
                if wait["protect"] == True: md+=" Protect : on\n"
                else: md+=" Protect : off\n"
                if wait["protectinv"] == True: md+=" Protectinv : on\n"
                else: md+=" Protectinv : off\n"
                if wait["protectqr"] == True: md+=" Protectqr : on\n"
                else: md+=" Protectqr : off\n"
                if wait["contact"] == True: md+=" Contact : on\n"
                else: md+=" Contact : off\n"
                if wait["autoJoin"] == True: md+=" Auto join : on\n"
                else: md +=" Auto join : off\n"
                if wait["leaveRoom"] == True: md+=" Auto leave : on\n"
                else: md+=" Auto leave : off\n"
                if wait["timeline"] == True: md+=" Share : on\n"
                else:md+=" Share : off\n"
                if wait["autoAdd"] == True: md+=" Auto add : on\n"
                else:md+=" Auto add : off\n"
                if wait["commentOn"] == True: md+=" Comment : on\n"
                else:md+=" Comment : off\n"
                cl.sendText(msg.to,md)
											
            elif msg.text in ["Group id","group id"]:
                gid = cl.getGroupIdsJoined()
                h = ""
                for i in gid:
                    h += "[%s]:%s\n" % (cl.getGroup(i).name,i)
                cl.sendText(msg.to,h)
								
            elif msg.text in ["Cancelall"]:
              if msg.from_ in admin:
                gid = cl.getGroupIdsInvited()
                for i in gid:
                    cl.rejectGroupInvitation(i)
                    print "SEND CANCELALL"
                if wait["lang"] == "JP":
                    cl.sendText(msg.to,"All invitations have been refused")
                else:
                    cl.sendText(msg.to,"æ‹’ç»äº†å…¨éƒ¨çš„é‚€è¯·ã€‚")
																			
            elif "Autocancel" in msg.text:
                try:
                    strnum = msg.text.replace("Autocancel","")
                    if strnum == "off":
                        wait["autoCancel"]["on"] = False
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,"Invitation refused turned off\nTo turn on please specify the number of people and send")
                        else:
                            cl.sendText(msg.to,"关了邀请拒绝。要时开请指定人数发送")
                    else:
                        num =  int(strnum)
                        wait["autoCancel"]["on"] = True
                        if wait["lang"] == "JP":
                            cl.sendText(msg.to,strnum + "The group of people and below decided to automatically refuse invitation")
                        else:
                            cl.sendText(msg.to,strnum + "使人以下的小组用自动邀请拒绝")
                except:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Value is wrong")
                    else:
                        cl.sendText(msg.to,"Bizarre ratings")		
												
            elif msg.text in ["Like:on"]:
                if wait["likeOn"] == True:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Done。")
                else:
                    wait["likeOn"] = True
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Already。")
            elif msg.text in ["Like:off"]:
                if wait["likeOn"] == False:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Done。")
                else:
                    wait["likeOn"] = False
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Already。")
												

            elif "admin add @" in msg.text:
                if msg.from_ in admin:
                    print "[Command]Staff add executing"
                    _name = msg.text.replace("admin add @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    gs = ki.getGroup(msg.to)
                    gs = kk.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Contact not found")
                    else:
                        for target in targets:
                            try:
                                admin.append(target)
                                cl.sendText(msg.to,"已給權")
                            except:
                                pass
                    print "[Command]Staff add executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Admin permission required.")

            elif "Admin add @" in msg.text:
                if msg.from_ in admin:
                    print "[Command]Staff add executing"
                    _name = msg.text.replace("Ar Staff add @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    gs = ki.getGroup(msg.to)
                    gs = kk.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Contact not found")
                    else:
                        for target in targets:
                            try:
                                admin.append(target)
                                cl.sendText(msg.to,"已給權")
                            except:
                                pass
                    print "[Command]Staff add executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Admin permission required.")

            elif "admin remove @" in msg.text:
                if msg.from_ in admin:
                    print "[Command]Staff remove executing"
                    _name = msg.text.replace("admin remove @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    gs = ki.getGroup(msg.to)
                    gs = kk.getGroup(msg.to)
                    targets = []
          
                    if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Contact not found")


                    else:
                        for target in targets:
                            try:
                                admin.remove(target)
                                cl.sendText(msg.to,"已移除")
                            except:
                                pass
                    print "[Command]Staff remove executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Admin permission required.")

            elif "Admin remove @" in msg.text:
                if msg.from_ in admin:
                    print "[Command]Staff remove executing"
                    _name = msg.text.replace("Admin remove @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    gs = ki.getGroup(msg.to)
                    gs = kk.getGroup(msg.to)
                    gs = kc.getGroup(msg.to)
                    gs = ks.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        ki.sendText(msg.to,"Contact not found")
                    else:
                        for target in targets:
                            try:
                                admin.remove(target)
                                cl.sendText(msg.to,"已移除")
                            except:
                                pass
                    print "[Command]Staff remove executed"
                else:
                    cl.sendText(msg.to,"Command denied.")
                    cl.sendText(msg.to,"Admin permission required.")

            elif msg.text in ["Adminlist","adminlist"]:
                if admin == []:
                    cl.sendText(msg.to,"The stafflist is empty")
                else:
                    cl.sendText(msg.to,"Permission list:")
                    mc = ""
                    for mi_d in admin:
                        mc += "->" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,mc)
                    print "[Command]Stafflist executed"
										
#-------------------------------------------------------------------------#									
        if op.type == 17:
            if op.param2 in Bots:
                return
            ginfo = cl.getGroup(op.param1)
            cl.sendText(op.param1, "ยินดีต้อนรับ สู่ กลุ่ม " + str(ginfo.name))
            print "สมาชิกเข้าร่วม"	
	
	if op.type == 15:
            random.choice(KAC).sendText(op.param1, cl.getContact(op.param2).displayName + ", โชคดี นะ แล้วพบกันใหม่\n(*´･ω･*)")
            print op.param3 + "has left the group"
        if op.type == 17:
            random.choice(KAC).sendText(op.param1, cl.getContact(op.param2).displayName + ", สวัสดีจร้า ")
            print op.param3 + "has left the group"
						
        if op.type == 11:
	    if op.param2 in Bots:
		return																           																				 									
#-------------------------------------------------------------------------#
        if op.type == 59:
            print op


    except Exception as error:
        print error

#-------------------------------------------------------------------------#   
while True:
    try:
        Ops = cl.fetchOps(cl.Poll.rev, 5)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(cl.Poll.rev))

    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            cl.Poll.rev = max(cl.Poll.rev, Op.revision)
            bot(Op)
            
#-------------------------------------------------------------------------#            
