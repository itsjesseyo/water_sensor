from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import json as JSOND

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

#added specifically to allow simple angular templatesin our jinja templates
from jinja2 import evalcontextfilter, Undefined, is_undefined

class TriangleUndefined(Undefined):
	"""
	Implements a specific `Undefined` class.
	If a variable in your Jinja2 template does not exists, trying to access a
	property will raise an `AttributeError`. This class implements a mechanism
	to prevent this behavior and return a `TriangleUndefined` object when you
	try to access a property of a `TriangleUndefined` object.
	The full name of a property is stored to keep a track of it :
		>>> test = TriangleUndefined(name=test) # this is how it's initialized
		>>> test.demo.for.the.documentation
		Undefined
		>>> test.demo.for.the.documentation._undefined_name
		u'test.demo.for.the.documentation'
	This "magic" class is used by the `angular_filter` to let the user easily
	define its client side template.
	"""

	def __getattr__(self, name):
		if name[1] == '_':
			raise AttributeError(name)
		return TriangleUndefined(name='{}.{}'.format(self._undefined_name,name))

def angular_filter(value):
	"""
	A filter to tell Jinja2 that a variable is for the AngularJS template
	engine.
	If the variable is undefined, its name will be used in the AngularJS
	template, otherwise, its content will be used.
	"""

	if is_undefined(value):
		return '{{{{{}}}}}'.format(value._undefined_name)
	if type(value) is bool:
		value = repr(value).lower()
	print 'angualr filter'
	return '{{{{{}}}}}'.format(value)


app.jinja_env.undefined = TriangleUndefined
app.jinja_env.filters['angular'] = angular_filter
socketio = SocketIO(app)

######################################################
#################### EXAMPLES ########################
######################################################
# #from flask quickstart http://flask.pocoo.org/docs/0.10/quickstart/
# @app.route('/')
# def hello_world():
# 		return 'Hello World!'

# #just showing how to load a template
# @app.route('/test_template')
# @app.route('/test_template/<name>')
# def test_template(name=None):
# 	return render_template('hello.html', name=name)


#from flask-scoketio getting started : https://flask-socketio.readthedocs.org/en/latest/

# #they arent very clear, but you generally first serve a webpage that ha some javascript in it that triggers the socket stuff form the client side
# @app.route('/hello_sockets')
# def hello_sockets():
# 		return render_template('hello_sockets.html')

# # this will come from client
# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))

######################################################
#################### OUR APP #########################
######################################################

client_list = []

#hacking together a barebones angular example from this : https://realpython.com/blog/python/flask-by-example-integrating-flask-and-angularjs/
@app.route('/home')
def index():
	return render_template('angular_with_sockets.html')

@socketio.on('connect')
def connect():
	print 'someone has joined the server'


@socketio.on('connection')
def connection(message):
	print 'someone has joined the server'
	if message not in client_list:
		client_list.append(message)
	emit('broadcast_client_list', client_list, broadcast=True)

# # this will come from client
# @socketio.on('ping_server')
# def ping_server(json):
# 	print('client says: ' + str(json))
# 	if json['data'] not in client_list:
# 		client_list.append(json['data'])
# 	emit('broadcast_client_list', client_list, broadcast=True)

# this will come from client
@socketio.on('receiving_sensor_update')
def receiving_sensor_update(json):
	print('sensor says: ' + str(json))


# this will come from client
@socketio.on('atime')
def atime(message):
	print('sensor says: ' + str(message))
	emit('atime', message, broadcast=True)

# this will come from client
@socketio.on('JSON')
def JSON(json):
	print('sensor says: ' + str(json))
	emit('JSON', json, broadcast=True)


if __name__ == '__main__':
	socketio.debug = False
	socketio.run(app, host='0.0.0.0', port=1234)










