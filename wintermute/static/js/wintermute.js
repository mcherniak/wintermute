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


Wintermute.controller('mainController', ['$scope', function($scope) {

    $scope.some_text = "testing"

}]);
