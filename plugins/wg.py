from asyncore import file_dispatcher
from dataclasses import _MISSING_TYPE
from doctest import OutputChecker
from genericpath import exists
from inspect import ArgSpec
from re import X
from errbot import BotPlugin, botcmd, arg_botcmd, backends
import sys,os, subprocess, qrcode,time

import telegram

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


   def qrshow(self, mesg, qrpath):
      qrcodefd = open(qrpath, "rb")
      stream = self.send_stream_request(mesg.frm, qrcodefd, name='image' , stream_type='photo' )

   def configshow(self, mesg, filename):
      f = open(filename, "r")
      stream = self.send_stream_request(mesg.frm, f, name='wg.conf',  stream_type='document' )
      id = self.build_identifier("85745624")
      

   def systemctl_do(self, action, name):
      subprocess.check_output(["systemctl", action, name], universal_newlines=True, cwd="/root",shell=True)
   
   def showall(self,mesg, filename, qrname):
      self.configshow(mesg, filename)
      self.qrshow(mesg, qrname)

   @botcmd
   def wg(self, mesg, args):
      name = str(mesg.frm.username)
      if name == "None":
         return "Для работы с WireGuard необходимо зарегистрировать имя пользователя в Telegram. Для этого в настройках аккаунта Telegram в поле \"Имя пользователя\" введите свое имя пользователя в системе. После этого перезапустите бота нажав /start."
      devicename = args
      if not devicename:
         devicename ="main"
      filename =  "wgclient_"+ name +"_"+ str(devicename) +  ".conf"
      qrname =  "wgclient_" + name +"_"+ str(devicename) + ".conf.qr.png"
      qrpath = "/root/"+qrname
      configpath = "/root/"+filename
      fullname = name + "_" + devicename


      if os.path.exists(configpath):
         if os.path.exists(qrpath):
            self.send(mesg.frm, "Конфиг был, код есть, всё хорошо")
            self.showall(mesg, configpath, qrpath)
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")
         else: 
            self.send(mesg.frm, "Конфиг был, кода нет, создаю код")
            self.qrcreate(configpath)
            self.showall(mesg, configpath, qrpath)
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")
            
      
      else:
            self.configcreate(mesg, fullname)
            self.qrcreate(configpath)
            
            self.systemctl_do("restart", "wg-quick@wghub.service")
            self.send(mesg.frm, "Конфиг создан, код создан, всё хорошо")
            
            self.showall(mesg, configpath, qrpath)
            self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
            time.sleep(3)
            self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")


   
   def device_create(self, mesg, args):
         name = str(mesg.frm.username)
         devicename = device
         filename =  "wgclient_"+ name +"_"+ devicename +  ".conf"
         qrname =  "wgclient_" + name +"_"+ devicename + ".conf.qr.png"
         qrpath = "/root/"+qrname
         configpath = "/root/"+filename
         fullname = name + "_" + devicename

         self.configcreate(mesg, fullname)
         self.systemctl_do("restart", "wg-quick@wghub.service")
         self.qrcreate(configpath)
         self.showall(mesg, configpath, qrpath)
         self.send(mesg.frm, "Инструкция по подключению тут: https://telegra.ph/Kak-podklyuchitsya-k-wireguard-na-android-smartfone-04-15 . Для работы нужно поставить приложение WireGuard и импортировать конфигурацию из файла wgclient_имя_устройства.conf. После этого нужно включить VPN и подключиться к серверу. Всё, можно пользоваться ужасным российским интернетом с СОРМ, ТСПУ, роскомнадзором и блокировочками.")
         time.sleep(3)
         self.send(mesg.frm, "Если что-то идёт не так - пиши @derunix")
         self.systemctl_do("restart", "wg-quick@wghub.service")

   @botcmd
   def start(self, mesg, args):
      id = self.build_identifier("85745624")
      self.send(id, "Юзер @" + str(mesg.frm.username) + " запустил бота")
      self.send(mesg.frm, "Привет, я бот, который создаёт конфиги для WireGuard. Напиши /wg для создания конфига, а дальше я всё тебе расскажу. Если что-то идёт не так - пиши @derunix")
      self.send(mesg.frm, "Если ты хочешь создать конфиг для другого устройства, напиши /wg devicename")
      self.send(mesg.frm, "Если ты хочешь дать мне денег, напиши /donate")
      self.send(mesg.frm, "По всем вопросам пиши сначала мне /help, а потом - @derunix . Наслаждайтесь вашим чем-то там!")



   @botcmd 
   def fix(self, mesg, args):
      try:
         counter = self[mesg.frm.username]
      except:
         counter = "0"
         self[mesg.frm.username] = counter

      if int(counter) < 1:
         self.send(mesg.frm, "Уверен что нужно? Это может сломать всё. Напиши /fix ещё раз")
         counter = int(counter) + 1
         self[mesg.frm.username] = str(counter)
      elif int(counter) <= 2:
         self.send(mesg.frm, "Поехали")
         self.systemctl_do("restart", "wg-quick@wghub.service")
         self[mesg.frm.username] = "2"
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + mesg.frm.username + " перезапустил WireGuard")
         self.send(mesg.frm, "Я всё исправил к худшему. Если нет - пиши @derunix")
         self[mesg.frm.username] = "3"
      elif int(counter) > 3 and int(counter) < 7:
         counter = self[mesg.frm.username]
         self.send(mesg.frm, "Тут не исправить уже ничего. Пиши @derunix")
         counter = int(counter) + 1
         self[mesg.frm.username] = str(counter)
         counter = self[mesg.frm.username]
      elif int(counter) == 7:
         id = self.build_identifier("85745624")
         counter = self[mesg.frm.username]
         self.send(mesg.frm, "Ой...")
         time.sleep(2)
         self.send(mesg.frm, "Ты пытаешься сломать мой бот?")
         time.sleep(4)
         self.send(mesg.frm, "Может что и получится...")
         self.send(id, "Юзер @" + mesg.frm.username + " молет о помощи")
         time.sleep(60)
         self.send(mesg.frm, "Ваши молитвы услышаны. Наши специалисты уже работают над этим. ")
         time.sleep(4)
         self.send(mesg.frm, "Наверное...")
         counter = int(counter) + 1
         self[mesg.frm.username] = str(counter)
         counter = self[mesg.frm.username]
      elif int(counter) > 8 and int(counter) < 20:
         self.send(mesg.frm, "Всё. Я устал. Попробуй завтра ещё раз. Или донат отправь, вдруг поможет. Жми /donate что бы узнать как.")
         time.sleep(0)
         
         counter = int(counter) + 1

         self[mesg.frm.username] = str(counter)
      elif int(counter) == 20:
         counter = self[mesg.frm.username]
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + str(mesg.frm.username) + " настойчиво молет о помощи")
         time.sleep(0)
         self.send(mesg.frm, "Хорошо. Я сделаю всё чтобы ты не мог больше ничего сломать")
         time.sleep(0)
         self.send(mesg.frm, "Но это будет стоить тебе 1000 рублей. Согласен?")
         self.send(mesg.frm, "Если да, то напиши /yes")
         self.send(mesg.frm, "Если нет, то напиши /no")
         self[mesg.frm.username] = "21"
      elif int(counter) >= 21:
         counter = self[mesg.frm.username]
         self.send(mesg.frm, "Осталось только подождать. Я уже знаю что тут можно ещё сделать. Я же просто бот раздающий впн..")
         time.sleep(0)
         return()
      else:
         counter = self[mesg.frm.username]
         counter = int(counter) + 1
         self[mesg.frm.username] = str(counter)
         


   @botcmd
   def donate(self, mesg, args):
      id = self.build_identifier("85745624")
      self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить")
      self.send(mesg.frm, "Если хочешь помочь мне, то можешь сделать это здесь: https://www.tinkoff.ru/cf/8IVGtFudrOz или на карту 5536913864711185")
      self.send(mesg.frm, "Ну или криптой: USDT(TRC20): TWjz74jg1t7osCn3DBVtnBU256SvT2bE4E . Может ещё какую-то крипту добавлю, если надо. Напиши @derunix если что")
   @botcmd      
   def yes(self,mesg,args):
         self.send(mesg.frm, "Спасибо за понимание")
         self.send(mesg.frm, "Вот номер карты: 5536913864711185")
         self.send(mesg.frm, "Уведомление отправлено. Ждите ответа")
         id = self.build_identifier("85745624")
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         self.send(mesg.frm, "Ждите ответа")
         time.sleep(10)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         time.sleep(60)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         time.sleep(300)
         self.send(id, "Юзер @" + str(mesg.frm.username) + " хочет донатить и быстрый ремонт!")
         self.send(mesg.frm, "Три раза уже напомнил ему.")
   @botcmd
   def no(self,mesg,args):
         self.send(mesg.frm, "Ну и ладно. Я не принуждаю")
         self[mesg.frm.username] = "100"
   
   @botcmd (admin_only=True)
   def fix_reset(self, mesg, args):
         counter = "0"
         self.send(mesg.frm, "Cчётчик пользователя @" + args +". Обнуляем!")
         self.send(mesg.frm, "Счётчик @"+args+ ": " + str(counter))
         self[args] = counter
   
   @botcmd (admin_only=True)
   def show(self, mesg, args):
         counter = "0"
         out = subprocess.check_output("wg" , shell=True, universal_newlines=True, stderr=subprocess.STDOUT)
         
         self.send(mesg.frm, out)

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
