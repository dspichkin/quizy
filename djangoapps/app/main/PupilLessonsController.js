'use strict';

var _ = require('lodash-node');
var Lesson = require('../models/lesson');

var PupilLessonsCtrl = function($scope, $mdDialog, $http, $data, $log, $location) {

    $scope.model = {
        lessons: [],

    };

    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.reset_menu();
                $location.path('/');
                return;
            }
        });
    }

    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';


    $scope.load_lesson = function(callback) {
        if ($scope.user.account_type == 2) {
            $http.get('/api/mylessons/').then(function(data) {
                $scope.model.lessons = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    data.data[i].created_at = Date.parse(data.data[i].created_at);
                    $scope.model.lessons.push(data.data[i]);
                }

                //console.log($scope.model.lessons)
            }, function(error) {
                $log.error('Ошибка получения назначенных на меня уроков', error);
            });
        }
    };

    $scope.play_lesson = function(enroll_id) {
        $location.path('/play/' + enroll_id + '/');
    };





    // =============================
    $scope.load_lesson();

}


module.exports = ['$scope', '$mdDialog', '$http', '$data', '$log', '$location', PupilLessonsCtrl];
