FLASK SETUP:

Create project directory and server directory within it. Copy app.py into server.

pip install Flask-Cors==3.0.4 
(for cross-origin requests - requests that originate from diff protocol, IP addr, domain name, port)





VUE SETUP (scroll to Vue Setup):
https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs

Summary for basic project setup:
1. install npm
2. npm install -g vue-cli@2.9.3
3. WITHIN PROJECT DIRECTORY: vue init webpack client
4. answer questions to create new project

Additional installs:
npm install --save axios@0.18.0 
(to communicate with Flask, use axios library to send AJAX requests)
npm install --save bootstrap@4.1.1
npm install --save bootstrap-vue@2.0.0-rc.11



Once you have setup a basic project, update the following folders with the files found in this Github directory:
- client>src>components --> add in Books.vue, Alert.vue, Ping.vue
- client>src>router --> update index.js
- client>src --> update App.vue
- server --> add in app.py


RUN:
1. in one terminal window, navigate to server and run app.py
2. in another window, navigate to client and run:
	npm run dev

See screenshots of sample run in demo imgs folder. 
Update and Delete buttons have not been implemented.


