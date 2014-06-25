'use strict';


var controller = Order.controller('controller', function($scope, $window, RestService, $location, $anchorScroll, $timeout){
    //handle the jump to the focused html tag
    $scope.scrollTo = function(id) {
      $location.hash(id);
      $anchorScroll();
    }

    //common network failure callbacks
    var failureCallback = function(status) {
        console.log(status);
    }

    //------------------------------------------/
    // init method
    //------------------------------------------/
    $scope.init = function(){
    }
})