'use strict';

var _ = require('lodash-node');
var Pupil = require('../models/pupil');

var TeacherPupilCtrl = function($scope, $mdDialog, $http, $data, $log, $location) {
    $scope.model = {
        pupils: []
    };



    if (!$scope.user || !$scope.user.is_authenticated) {
        $.ajax({
            type: "GET",
            url: '/api/user/',
            async: false
        }).then(function(data) {
            $scope.user = {
                username: 'guest',
                is_authenticated: false,
                loaded: false
            };

            $scope.user = data;
            $scope.user.loaded = true;

        }, function(error) {
            $log.error('Ошибка получения данных', error);
        });

    }

    $scope.main.make_short_header();
    $scope.main.active_menu = 'pupils';


    $scope.load_pupils = function(callback) {
        if ($scope.user.account_type == 1) {
            $http.get('/api/pupils/').then(function(data) {
                $scope.model.pupils = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    $scope.model.pupils.push(new Pupil(data.data[i]));
                }

            }, function(error) {
                $log.error('Ошибка получения курсов', error);
            });
        } else {
            $location.path('/');
        }
    };


    // =================================
    $scope.load_pupils();

}



module.exports = ['$scope', '$mdDialog', '$http', '$log', '$location', TeacherPupilCtrl];

