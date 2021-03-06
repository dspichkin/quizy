'use strict';
/* globals
require:false,
$:false,
module:false
*/
var _ = require('lodash-node');
var Lesson = require('../models/lesson');

var PupilLessonsCtrl = function($scope, $mdDialog, $http, $data, $log, $location, $timeout) {

    $scope.model = {
        lessons: [],
        nolessons: false,
        loaded: false
    };


    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    } else if ($scope.user.account_type != 2 && $scope.user.account_type != 1) {
        console.log('$scope.user.account_type', $scope.user.account_type)
        $scope.main.go_home_page();
        return;
    }


    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';


    $scope.load_lessons = function(callback) {
        if ($scope.user.account_type == 2 || $scope.user.account_type == 1) {
            $http.get('/api/mylessons/').then(function(data) {
                $scope.model.lessons = [];
                if (data.data.length > 0) {
                    for (var i = 0, len = data.data.length; i < len; i++) {
                        data.data[i].created_at = Date.parse(data.data[i].created_at);
                        $scope.model.lessons.push(data.data[i]);
                    }
                } else {
                    $scope.model.nolessons = true;
                }
                $scope.model.loaded = true;
                //console.log($scope.model.lessons)
            }, function(error) {
                $log.error('Ошибка получения назначенных на меня уроков', error);
                $scope.model.loaded = true;
            });
        }
    };

    $scope.play_lesson = function(enroll_id) {
        $timeout(function() {
            $location.path('/play/' + enroll_id + '/');
        }, 500);
        
    };


    $scope.reject_lesson = function($event, lesson_id) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/confirm/confirm_reject_lesson.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.model.modal = {
                    loading: false
                };
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };

                $scope.submit = function($event) {
                    $scope.model.modal.loading = true;
                    $.post('/api/reject_lesson/' + lesson_id + '/').then(function(data) {
                        $scope.model.modal.loading = false;
                        $scope.load_lessons();
                        $mdDialog.hide();
                    }, function(error) {
                        $scope.model.modal.loading = false;
                        $log.error(error);
                        $scope.load_lessons();
                        $mdDialog.hide();
                    });
                };

            }
        });
    };

    $scope.to_archive = function($event, lesson_id) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/confirm/confirm_archive_lesson.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.model.modal = {
                    loading: false
                };
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };

                $scope.submit = function($event) {
                    $scope.model.modal.loading = true;
                    $.post('/api/reject_lesson/' + lesson_id + '/').then(function(data) {
                        $scope.model.modal.loading = false;
                        $scope.load_lessons();
                        $mdDialog.hide();
                    }, function(error) {
                        $scope.model.modal.loading = false;
                        $log.error(error);
                        $scope.load_lessons();
                        $mdDialog.hide();
                    });
                };

            }
        });
    };

    /*
    $scope.to_archive = function($event, lesson_id) {
        $.post('/api/reject_lesson/' + lesson_id + '/').then(function(data) {
            $scope.load_lessons();
            $mdDialog.hide();
        }, function(error) {
            $scope.model.modal.loading = false;
            $log.error(error);
            $scope.load_lessons();
            $mdDialog.hide();
        });
    };

    */


    // =============================
    $scope.load_lessons();

};


module.exports = ['$scope', '$mdDialog', '$http', '$data', '$log', '$location', '$timeout',PupilLessonsCtrl];
