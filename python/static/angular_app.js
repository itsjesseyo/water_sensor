(function () {
	//this self calling functions is the javascript way to create a locally scoped "module"
	//variables declared here are only available to the javascript in this module
	//jquery works the same way but assigns the module instance to the "$" sign

	'use strict';// you should just always use this
	var app = angular.module('MyApp', []);//the "global" app instance. we just use it to add controllers, routes, etc.

	//this controller is the root controller for the html page.
	//html pages can have several controllers, one, or none.
	//a single contnorller can be used on many html pages, but it gets loaded as a unique instace.
	app.controller('MyController', function($scope){

		$scope.socket_clients = [];
		$scope.my_time = '';
		$scope.my_json = '';

		//the ng-click attribute was added in html to trigger this function
		//this way your javascript is cleanyl separated.
		//the downside is you have to track your special html attributes
		$scope.PingButtonClicked = function(){
			console.log("button clicked");
			socket.emit('connection', 'frank the website');
		};

		$scope.FakeATime = function(){
			console.log("button clicked");
			socket.emit('atime', "KJ$##)CN");
		};

		$scope.FakeJSON = function(){
			console.log("button clicked");
			socket.emit('JSON', {data: 'frank the website'});
		};

		socket.on('broadcast_client_list', function(data) {
			console.log('updating client list:' + data);
			$scope.socket_clients = data;
			$scope.$apply();
		});

		socket.on('atime', function(data) {
			console.log('caught time broadcast' + data);
			$scope.my_time = data;
			$scope.$apply();
		});

		socket.on('JSON', function(data) {
			console.log('caught json broadcast' + data['data']);
			$scope.my_json = JSON.stringify(data);
			$scope.$apply();
		});

	});


})();