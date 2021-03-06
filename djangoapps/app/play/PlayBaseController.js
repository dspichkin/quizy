'use strict';
/* globals
require:false,
$:false,
app:false,
module:false
*/
var Page = require('../models/page');
var Lesson = require('../models/lesson');
var Attempt = require('../models/attempt');

var PlayCtrl = function($scope, $stateParams, $http, $compile, $log) {

    /*
    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    }
    */

    $scope.show_debug = false;

    $scope.model.play = {
        path: null,
        template: null,
        controller: null,
        lesson_type: null,
        course_id: null
    };


    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';



    start();


    $scope.getController = function() {
        return 'ControllerName';
    };

    $scope.getTemplate = function() {
        return $scope.model.play.template;
    };

    function load_enroll(enroll_id) {
        return $http.get('/api/play/' + enroll_id + "/").then(function(data) {
            $scope.model.play.enroll = data.data;
            start_content(data);

            }, function(error) {
                $log.error('PlayBaseController: Ошибка получения назначенных уроков', error);
                $scope.main.go_home_page();
            });
    }

    function start_content(data) {
        $scope.model.play.lesson_type = data.data.lesson.lesson_type;
        $scope.model.play.course_id = data.data.lesson.course;
        if (data.data.lesson.lesson_type == 'outside') {
            $scope.model.play.path = data.data.lesson.content.path;
            $scope.model.play.template = $scope.model.play.path + data.data.lesson.content.template;
            $scope.model.play.controller = $scope.model.play.path + data.data.lesson.content.controller;
            $scope.model.play.enroll = data.data;
            var jsLink = $("<script type='text/javascript' src='" + $scope.model.play.controller + "'>");
            $("head").append(jsLink);
            // Регистрация контроллера
            app.controllerProvider.register('ControllerName', app.ControllerName);
        }
        if (data.data.lesson.lesson_type == 'inside') {
            $scope.model.play.template = '/assets/partials/play/play.html';
        }
    }


    function load_lesson(lesson_id, callback) {

        return $http.get('/api/demo/play/' + lesson_id + "/").then(function(data) {
                if (!data.data.lesson.lesson_type) {
                    $log.error("Ошибка определения типа урока");
                }
                start_content(data);
            }, function(error) {
                $log.error('Ошибка получения назначенния уроков', error);
            });
    }

    function load_public_lesson(public_lesson_id, callback) {
        return $http.get('/api/public/play/' + public_lesson_id + "/").then(function(data) {
            
            if (!data.data.type) {
                $log.error("Ошибка определения типа урока");
            }
            if (data.data.type == 'enroll') {
                $scope.main.go_play(data.data.id);
            }
            if (data.data.type == 'lesson') {
                data.data.lesson = data.data;
                $scope.model.play.enroll = data.data;
                start_content(data);
            }

        }, function(error) {
            $log.error('Ошибка получения назначенния уроков', error);
        });
    }


    function start() {
        $scope.model.play.current_page_index = 0;
        if ($stateParams.enroll_id) {
            load_enroll($stateParams.enroll_id);
        } else if ($stateParams.lesson_id) {
            load_lesson($stateParams.lesson_id);
        } else if ($stateParams.public_lesson_id) {
            load_public_lesson($stateParams.public_lesson_id);
        } else {
            return;
        }
    }


    $scope.back_to_lessons = function() {
        if ($stateParams.lesson_id) {
            $scope.main.go_courses_page($scope.model.play.course_id);
        }

    };
    $scope.back_to_editor = function() {
        if ($stateParams.lesson_id) {
            if ($scope.model.play.lesson_type == 'inside') {
                $scope.main.go_editor_lesson($stateParams.lesson_id);
            }
        }

    };





};


module.exports = ['$scope', '$stateParams', '$http', '$compile', '$log', PlayCtrl];


