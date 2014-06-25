'use strict';

/* Services */

Order.factory('RestService', function($http, $q){
    return {
        addItem: function(oid, post){
            var url = '/rest/item/{}/add/'.format(oid);
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: post}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        updateItem: function(oid, post){
            var url = '/rest/item/{}/update/'.format(oid);
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: post}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        removeItem: function(oid, post){
            var url = '/rest/item/{}/remove/'.format(oid);
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: post}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        }
    }
});

Order.factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    }
	return vars;
});