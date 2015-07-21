'use strict';

var _ = require('lodash-node');
var Course = require('../models/course');

var CourseCtrl = function($scope, $mdDialog, $http, $log, $location, $stateParams) {
    $scope.model = {

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
    $scope.main.active_menu = 'courses';






    $scope.load_course = function(callback) {
        if ($stateParams.course_id) {
            $http.get('/api/courses/' + $stateParams.course_id + '/').then(function(data) {
                $scope.model.course = new Course(data.data);

                console.log("!",  $scope.model.course)

            }, function(error) {
                $log.error('Ошибка получения уроков', error);
            });
        } else {
            return;
        }
    };



    // =============================
    $scope.load_course();


};

module.exports = ['$scope', '$mdDialog', '$http', '$log', '$location', '$stateParams', CourseCtrl];


