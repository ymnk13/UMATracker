(function(angular) {
    'use strict';
    var myApp = angular.module('myApp', ['ngAnimate']);
    myApp.controller('changeView',  ['$scope', function($scope){
	$scope.mainUrl = "./partials/documents.html";
	$scope.getLink = function(index){
	    $scope.scene = index;
	    $scope.mainUrl = './partials/'+index+'.html';
	    console.log(index)
	    //console.log($scope.mainUrl);
	}
	$scope.setLink = function(){
	    //console.log($scope.scene);
	}
    }]);
})(window.angular);
