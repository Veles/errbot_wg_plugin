from asyncore import file_dispatcher
from dataclasses import _MISSING_TYPE
from doctest import OutputChecker
from genericpath import exists
from inspect import ArgSpec
from re import X
from errbot import BotPlugin, botcmd, arg_botcmd, backends
import sys,os, subprocess, qrcode,time

import telegram
############################################################################################################
##Create actions
############################################################################################################
class Wg(BotPlugin):
   def configcreate(self, mesg, filename):
         subprocess.check_output(["/root/easy-wg-quick", filename], universal_newlines=True, cwd="/root")
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + str(mesg.frm.username) + " создал конфигурацию " + filename)
         self.systemctl_do("restart", "wg-quick@wghub.service")

   def qrcreate(self, filename):
      qrcodefd = open(filename, "r")
      img = qrcode.make(qrcodefd.read())
      type(img)  # qrcode.image.pil.PilImage
      img.save(filename +".qr.png")

############################################################################################################
##Show actions
############################################################################################################
   def qrshow(self, mesg, qrpath):
      qrcodefd = open(qrpath, "rb")
      stream = self.send_stream_request(mesg.frm, qrcodefd, name='image' , stream_type='photo' )

   def configshow(self, mesg, filename):
      f = open(filename, "r")
      stream = self.send_stream_request(mesg.frm, f, name='wg.conf',  stream_type='document' )
      id = self.build_identifier("85745624")

   def showall(self,mesg, filename, qrname):
      self.configshow(mesg, filename)
      self.qrshow(mesg, qrname)      

############################################################################################################
##Systemctl actions
############################################################################################################
   def systemctl_do(self, action, name):
      subprocess.check_output(["systemctl", action, name], universal_newlines=True, cwd="/root",shell=True)

   @botcmd (admin_only=True)
   def show(self, mesg, args):
         counter = "0" #reset counter. Just in case
         out = subprocess.check_output("wg" , shell=True, universal_newlines=True, stderr=subprocess.STDOUT) #get output from wg
         self.send(mesg.frm, out) #send output to admin
   
   @botcmd (admin_only=True)
   def shell(self, mesg, args):
         counter = "0" #reset counter. Just in case
         out = subprocess.check_output(args , shell=True, universal_newlines=True, stderr=subprocess.STDOUT) #run shell command from args. Example: !shell ls -la
         self.send(mesg.frm, out) #send output to admin

############################################################################################################
## User commands
############################################################################################################
   @botcmd
   def wg(self, mesg, args):
      name = str(mesg.frm.username) 
      if name == "None": #if user has no username
         return "Для работы с WireGuard необходимо зарегистрировать имя пользователя в Telegram. Для этого в настройках аккаунта Telegram в поле \"Имя пользователя\" введите свое имя пользователя в системе. После этого перезапустите бота нажав /start."
      
      if args == "": #if no args   
         devicename ="main" #set default device name
      if args != "": #if args
         devicename = str(args) #set device name from args
      ##Variables
      filename =  "wgclient_"+ name +"_"+ str(devicename) +  ".conf"
      qrname =  "wgclient_" + name +"_"+ str(devicename) + ".conf.qr.png"
      qrpath = "/root/"+qrname
      configpath = "/root/"+filename
      fullname = name + "_" + devicename
      ##Check if config exists
      if os.path.exists(configpath): #if config exists return it
         if os.path.exists(qrpath): #if qr exists return it
            self.send(mesg.frm, "Конфиг был, код есть, всё хорошо")
            self.showall(mesg, configpath, qrpath) #send config and qr
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")
         if not os.path.exists(qrpath):   #if qr not exists create it and return qr
            self.send(mesg.frm, "Конфиг был, кода нет, создаю код")
            self.qrcreate(configpath) #create qr
            self.showall(mesg, configpath, qrpath) #send config and qr
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")      
      if not os.path.exists(configpath): #if config not exists create it and return it
            self.configcreate(mesg, fullname) #create config
            self.qrcreate(configpath) #create qr
            out = self.systemctl_do("restart", "wg-quick@wghub.service") #restart wg
            id = self.build_identifier("85745624")
            self.send(id, "Юзер @" + str(mesg.frm.username) + " создал конфигурацию для " + str(fullname) + " и перезапустил WireGuard") #send message to me
            self.send(id, out) #send output to me
            self.send(mesg.frm, "Конфиг создан, код создан, всё хорошо")
            self.showall(mesg, configpath, qrpath) #send config and qr
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")

############################################################################################################
## fix acions
############################################################################################################
   @botcmd (admin_only=True)
   def fix_fix(self, mesg, args):
         counter = "2" #counter for while
         self.send(mesg.frm, "Cчётчик пользователя @" + mesg.frm.username +". Обнуляем!")
         self.send(mesg.frm, "Счётчик @"+mesg.frm.username+ ": " + str(counter))
         self[mesg.frm.username] = counter #set counter to 2
         self.fix(mesg, args) #run fix immediately
         self[mesg.frm.username] = "0" #set counter to 0 for next time

   @botcmd 
   def fix(self, mesg, args): #user can try to restart wireguard
      try: #check existance of counter for user
         counter = self[mesg.frm.username]
      except:
         counter = "0" #if not exists, set it to 0
         self[mesg.frm.username] = counter #save it
      if int(counter) == 0: #safety first
         counter = self[mesg.frm.username]
         self.send(mesg.frm, "Уверен что нужно? Это может сломать всё. Напиши /fix ещё раз")
         counter = int(counter) + 1 #increase counter
         self[mesg.frm.username] = str(counter) #save it. Now counter is 1
      elif int(counter) == 1: #If counter is 1. User wrote /fix twice
         counter = self[mesg.frm.username] #get counter
         self.send(mesg.frm, "Поехали")
         self.systemctl_do("restart", "wg-quick@wghub.service") #Do it
         self[mesg.frm.username] = "2" #Set counter to 2. Prevents from doing it again
         id = self.build_identifier("85745624") #send message to me
         self.send(id, "Юзер @" + mesg.frm.username + " перезапустил WireGuard") #send message to me
         self.send(mesg.frm, "Я всё исправил к худшему. Если нет - пиши @derunix")
      elif int(counter) > 1 and int(counter) < 7: #If counter is 2-6. User wrote /fix more than twice
         counter = self[mesg.frm.username] #get counter
         self.send(mesg.frm, "Тут не исправить уже ничего. Пиши @derunix")
         counter = int(counter) + 1 #increase counter
         self[mesg.frm.username] = str(counter) #save it. Now counter is 3-7
         counter = self[mesg.frm.username] #get counter. It's 3-7
      elif int(counter) == 7: #If counter is 7. User wrote /fix more than 7 times
         id = self.build_identifier("85745624") #send message to me
         counter = self[mesg.frm.username] #get counter
         self.send(mesg.frm, "Ой...") 
         time.sleep(2)
         self.send(mesg.frm, "Ты пытаешься сломать мой бот?")
         time.sleep(4)
         self.send(mesg.frm, "Может что и получится...")
         self.send(id, "Юзер @" + mesg.frm.username + " молет о помощи") #send message to me
         time.sleep(60) #wait 60 seconds. It's enough to stop bot
         self.send(mesg.frm, "Ваши молитвы услышаны. Наши специалисты уже работают над этим. ")
         time.sleep(4)
         self.send(mesg.frm, "Наверное...")
         counter = int(counter) + 1 #increase counter. Now counter is 8
         self[mesg.frm.username] = str(counter) #save it. Now counter is 8
         counter = self[mesg.frm.username] #get counter. It's 8
      elif int(counter) > 8 and int(counter) < 20: #If counter is 8-19. User wrote /fix more than 8 times
         counter = self[mesg.frm.username] 
         self.send(mesg.frm, "Всё. Я устал. Попробуй завтра ещё раз. Или донат отправь, вдруг поможет. Жми /donate что бы узнать как.")
         time.sleep(60) #wait 60 seconds. It's enough to stop bot
         counter = int(counter) + 1 #increase counter. Now counter is 9-20
         self[mesg.frm.username] = str(counter) #save it. Now counter is 9-20
      elif int(counter) == 20: #If counter is 20. User wrote /fix more than 20 times
         counter = self[mesg.frm.username] #get counter. It's 20
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + str(mesg.frm.username) + " настойчиво молет о помощи") #send message to me. It's time to stop bot
         time.sleep(3) #wait 30 seconds. It's enough to stop bot
         self.send(mesg.frm, "Хорошо. Я сделаю всё чтобы ты не мог больше ничего сломать")
         time.sleep(6) #wait 60 seconds. It's enough to stop bot
         #make the deal with the devil
         self.send(mesg.frm, "Но это будет стоить тебе 1000 рублей. Согласен?")
         self.send(mesg.frm, "Если да, то напиши /yes") #red pill
         self.send(mesg.frm, "Если нет, то напиши /no") #blue pill
         self[mesg.frm.username] = "21" #set counter to 21. Now user can choose
      elif int(counter) >= 21: #If counter is 21 or more. User wrote /fix more than 20 times
         counter = self[mesg.frm.username] #get counter. It's 21 or more
         self.send(mesg.frm, "Осталось только подождать. Я уже знаю что тут можно ещё сделать. Я же просто бот раздающий впн..")
         time.sleep(600) #wait 600 seconds. It's enough to stop bot. User can't write /fix more than 20 times in 10 minutes
         return()
      else:   #If counter is 0. User wrote /fix first time
         counter = self[mesg.frm.username]
         counter = int(counter) + 1 #increase counter. Now counter is 1
         self.send(mesg.frm, "Уверен что нужно? Это может сломать всё. Напиши /fix ещё раз")
         self[mesg.frm.username] = str(counter) #save it. Now counter is 1


############################################################################################################
## Deal with the devil
############################################################################################################   

   @botcmd      
   def yes(self,mesg,args): #follow the white rabbit
         self.send(mesg.frm, "Спасибо за понимание")
         self.send(mesg.frm, "Вот номер карты: 5536913864711185")
         self.send(mesg.frm, "Уведомление отправлено. Ждите ответа")
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!") #send message to me. User wants to donate and fix vpn
         self.send(mesg.frm, "Ждите ответа")
         time.sleep(10)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         time.sleep(60)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         time.sleep(300)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         self.send(mesg.frm, "Три раза уже напомнил ему.")
   @botcmd
   def no(self,mesg,args): #the matrix has you...
         self.send(mesg.frm, "Ну и ладно. Я не принуждаю")
         self[mesg.frm.username] = "100" #save it. Now counter fix isnt working until admin clear counter
   
   @botcmd (admin_only=True)
   def fix_reset(self, mesg, args): #reset counter for user
         counter = "0" #reset counter
         self.send(mesg.frm, "Cчётчик пользователя @" + args +". Обнуляем!")
         self.send(mesg.frm, "Счётчик @"+args+ ": " + str(counter))
         self[args] = counter #save it

############################################################################################################
## User info commands
############################################################################################################

   @botcmd
   def start(self, mesg, args):
      id = self.build_identifier("85745624") 
      self.send(id, "Юзер @" + str(mesg.frm.username) + " запустил бота") #send message to me
      self.send(mesg.frm, "Привет, я бот, который создаёт конфиги для WireGuard. Напиши /wg для создания конфига, а дальше я всё тебе расскажу. Если что-то идёт не так - пиши @derunix")
      self.send(mesg.frm, "Если ты хочешь создать конфиг для другого устройства, напиши /wg devicename")
      self.send(mesg.frm, "Если ты хочешь дать мне денег, напиши /donate")
      self.send(mesg.frm, "По всем вопросам пиши сначала мне /help, а потом - @derunix . Наслаждайтесь вашим чем-то там!")

   @botcmd
   def donate(self, mesg, args): #must important command
      id = self.build_identifier("85745624")
      self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить")
      self.send(mesg.frm, "Если хочешь помочь мне, то можешь сделать это здесь: https://www.tinkoff.ru/cf/8IVGtFudrOz или на карту 5536913864711185")
      self.send(mesg.frm, "Ну или криптой: USDT(TRC20): TWjz74jg1t7osCn3DBVtnBU256SvT2bE4E . Может ещё какую-то крипту добавлю, если надо. Напиши @derunix если что")
      self.send(mesg.frm, "Если ты хочешь быстрый ремонт, то напиши /fix. Бот напомнит мне о твоей просьбе")

   @botcmd
   def help(self, mesg, args):
      id = self.build_identifier("85745624")
      self.send(id, "Юзер @" + str(mesg.frm.username) + " запустил бота")
      self.send(mesg.frm, "Привет, я бот, который создаёт конфиги для WireGuard. Напиши /wg для создания конфига")
      self.send(mesg.frm, "Если ты хочешь создать конфиг для другого устройства, напиши /wg devicename")
      self.send(mesg.frm, "Можно попробовать починить что-то, если что-то сломалось, напиши /fix. Но это не точно")
      self.send(mesg.frm, "Если хочешь помочь мне, то можешь сделать это здесь: https://www.tinkoff.ru/cf/8IVGtFudrOz или на карту 5536913864711185")
      self.send(mesg.frm, "Подробнее про донат можно прочитать здесь /donate")
      self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 .")
      self.send(mesg.frm, "По всем вопросам пиши @derunix . Наслаждайтесь вашим чем-то там!")
