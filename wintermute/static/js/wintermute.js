var Wintermute = angular.module('Wintermute', ['ngRoute']);
//Routes
Wintermute.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
    $routeProvider
        .when('/', {
            templateUrl: '/static/html/main.html',
            controller: 'mainController'
        })
}]);


Wintermute.controller('mainController', ['$scope', '$http', function($scope, $http) {

    $scope.some_text = "How are you doing"
    $scope.some_var = "this is a new var"

    $http.get("http://localhost:5000/api/helloworld/10.246.0.0/16")
          .success(function (response) {$scope.ip_network = response;});

}]);
