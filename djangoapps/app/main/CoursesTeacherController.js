'use strict';

var _ = require('lodash-node');
var Lesson = require('../models/lesson');
var Course = require('../models/course');

var CoursesCtrl = function($scope, $mdDialog, $http, $data, $timeout, $log, $location) {
    $scope.model = {
        courses: [],
        lessons_for_me: [],
        archive: [],
        show_user: true,
        inputed_address: "",
        show_invite: false,

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


    $scope.load_courses = function(callback) {
        if ($scope.user.account_type == 1) {
            $http.get('/api/courses/').then(function(data) {
                $scope.model.courses = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    $scope.model.courses.push(new Course(data.data[i]));
                }


                console.log("!", $scope.model.courses)

                

                
            }, function(error) {
                $log.error('Ошибка получения курсов', error);
            });
        }
    };

    $scope.go_course_lessons = function(course_id) {
        $location.path('/courses/' + course_id + '/');
    }



    // =============================
    $scope.load_courses();


};

module.exports = ['$scope', '$mdDialog', '$http', '$data', '$timeout', '$log', '$location', CoursesCtrl];


