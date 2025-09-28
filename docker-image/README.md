# Install podman on your linux server ( Remote server or could be your local machine )

   $ sudo apt install -y podman


# Pull down the container image from docker.io :

   $ podman pull docker.io/254in61/model-citizens-chatbot:latest


# Start the backend application
   
   $ podman run -p 5000:5000 docker.io/254in61/model-citizens-chatbot

   *** If having a running application binding the same port : $ kill -9 $(lsof -t -i :5000)

# Open the chat window on your browser : 
   
   $ http://ip_address_of_server:5000

   If this is running on your localhost : $ http://127.0.0.1:5000

   If it is running in a remote server, for example server ip is 192.168.1.98: $ http://192.168.1.98:5000
