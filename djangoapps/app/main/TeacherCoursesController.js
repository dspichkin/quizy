'use strict';

var _ = require('lodash-node');
var Course = require('../models/course');
var CoursesCtrl = function($scope, $mdDialog, $http, $data, $timeout, $log, $location) {
    $scope.model = {
        courses: [],
        lessons_for_me: [],
        archive: [],
        show_user: true,
        inputed_address: "",
        show_invite: false
    };

    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.reset_menu();
                $location.path('/');
                return;
            }
        });
    } else if ($scope.user.account_type == 2) {
        $location.path('/');
        return;
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
            }, function(error) {
                $log.error('Ошибка получения курсов', error);
            });
        }
    };

    $scope.go_course_lessons = function(course_id) {
        $location.path('/courses/' + course_id + '/');
    };

    $scope.course_enroll = function($event, course_id) {

        $scope.assign_course_id = course_id;
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/course/assign_course.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.model['modal_enroll'] = {
                    auto_enroll: false,
                    inputed_address: "",
                    show_error: false,
                    error_message: "",
                    show_create_account: false
                };

                $scope.get_mypupils = function() {
                    $.get('/api/get_mypupil/').then(function(data) {
                        $scope.model.modal_enroll.mypupils = data;
                        $scope.$digest();
                    },
                    function(error) {
                        $scope.model.modal_enroll.show_error = true;
                        $scope.model.modal_enroll.error_message = "Invalid request";
                        $scope.$digest();
                        $log.error(error);
                    });
                };

                $scope.select_pupil = function($index) {
                    $scope.model.modal_enroll.inputed_address = $scope.model.modal_enroll.mypupils[$index];
                    $scope.change_inputed_address();
                };

                $scope.get_mypupils();

                $scope.form_errors = {};
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };
                $scope.submit_disabled = true;
                $scope.change_inputed_address = function() {
                    if ($scope.model.modal_enroll.inputed_address != "") {
                        $scope.submit_disabled = false;
                    } else {
                        $scope.submit_disabled = true;
                    }
                };
                $scope.ok = function($event) {
                    var _data = {
                        course_id: $scope.assign_course_id,
                        email: $scope.model.modal_enroll.inputed_address,
                        auto_enroll: $scope.model.modal_enroll.auto_enroll
                    };
                    $scope.model.modal_enroll.loading = true;
                    $.post('/api/enroll_pupil/', JSON.stringify(_data)).then(function(data) {
                        $scope.model.modal_enroll.loading = false;
                        if (data.hasOwnProperty('code')) {
                            if (data.code == 404) {
                                $scope.model.modal_enroll.show_error = true;
                                $scope.model.modal_enroll.error_message = "Указаный вами email " +
                                    $scope.model.modal_enroll.inputed_address + " не найден среди зарегистрированных учеников.";
                                $scope.model.modal_enroll.show_create_account = true;
                                $scope.$digest();
                            }
                        } else {
                            $mdDialog.hide();
                            $scope.model.modal_enroll.show_error = false;
                            $scope.$digest();
                            $scope.load_courses();
                        }
                    }, function(error) {
                        $scope.model.modal_enroll.show_error = true;
                        $scope.model.modal_enroll.error_message = "Invalid request";
                        $scope.$digest();
                        $log.error(error);
                    });
                };

                scope.cancelCreateAccount = function($event) {
                    $scope.model.modal_enroll.show_create_account = false;
                    $scope.model.modal_enroll.inputed_address = null;
                    $scope.model.modal_enroll.error_message = null;
                    $scope.model.modal_enroll.show_error = false;
                };

                scope.createAccount = function($event) {
                    var _data = {
                        course_id: $scope.assign_lesson_id,
                        email: $scope.model.modal_enroll.inputed_address,
                        auto_enroll: $scope.model.modal_enroll.auto_enroll
                    };

                    $.post('/api/create_pupil/', JSON.stringify(_data)).then(function(data) {
                        $scope.model.modal_enroll.show_create_account = false;
                        $scope.model.modal_enroll.inputed_address = null;
                        $scope.model.modal_enroll.error_message = null;
                        $scope.model.modal_enroll.show_error = false;

                        $mdDialog.hide();
                        $scope.load_courses();
                    }, function(error) {
                        $scope.model.modal_enroll.show_error = true;
                        $scope.model.modal_enroll.error_message = "Invalid request";
                        $scope.$digest();
                        $log.error(error);
                    });
                };
            }
        });
    };



    // =============================
    $scope.load_courses();


};

module.exports = ['$scope', '$mdDialog', '$http', '$data', '$timeout', '$log', '$location', CoursesCtrl];


