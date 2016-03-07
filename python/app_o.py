from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import datetime
import json as JSON
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

#from flask-scoketio getting started : https://flask-socketio.readthedocs.org/en/latest/

#they arent very clear, but you generally first serve a webpage that ha some javascript in it that triggers the socket stuff form the client side
@app.route("/")
def hello():
    return render_template('sockets.html')

@socketio.on('connect')
def connected():
    emit('get_moisture_value', 'please') 

@socketio.on('update_moisture_value')
def received_time(json):
    json = JSON.loads(json)
    print "receiving moisture value from : " + json['device']
    print 'value is :' + json['value']

if __name__ == '__main__':
    socketio.debug = True
    socketio.run(app)







