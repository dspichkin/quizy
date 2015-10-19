'use strict';

var _ = require('lodash-node');
var Course = require('../models/course');

var CourseCtrl = function($scope, $mdDialog, $http, $log, $location, $stateParams) {
    $scope.model = {

    };


    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.go_home_page();
            }
        });
        return;
    } else if ($scope.user.account_type != 1) {
        $scope.main.go_home_page();
        return;
    }


    $scope.main.make_short_header();
    $scope.main.active_menu = 'courses';





    $scope.load_course = function(callback) {
        if ($stateParams.course_id) {
            $http.get('/api/courses/' + $stateParams.course_id + '/').then(function(data) {
                $scope.model.course = new Course(data.data);

                //console.log("!",  $scope.model.course)

            }, function(error) {
                $log.error('Ошибка получения уроков', error);
            });
        } else {
            return;
        }
    };


    $scope.lesson_enroll = function($event, lesson_id) {
        $scope.assign_lesson_id = lesson_id;
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/assign_lesson.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {
                    $scope.model['modal_enroll'] = {
                        inputed_address: "",
                        show_error: false,
                        error_message: "",
                        show_create_account: false
                    };

                    $scope.get_mypupils = function(email) {
                        var url = '/api/get_mypupil/';
                        if (email) {
                            url = '/api/get_mypupil/?email=' + email;
                        }
                        $.get(url).then(function(data) {
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
                        $scope.get_mypupils($scope.model.modal_enroll.inputed_address);

                        if ($scope.model.modal_enroll.inputed_address != "") {
                            $scope.submit_disabled = false;
                        } else {
                            $scope.submit_disabled = true;
                        }
                    };
                    $scope.ok = function($event) {
                        var _data = {
                            lesson_id: $scope.assign_lesson_id,
                            email: $scope.model.modal_enroll.inputed_address
                        };
                        $scope.model.modal_enroll.loading = true;
                        $.post('/api/enroll/', JSON.stringify(_data)).then(function(data) {
                            $scope.model.modal_enroll.loading = false;

                            if (data.hasOwnProperty('code')) {
                                if (data.code == 404) {
                                    $scope.model.modal_enroll.show_error = true;
                                    $scope.model.modal_enroll.error_message = "Указаный вами email " +
                                        $scope.model.modal_enroll.inputed_address + " не найден среди зарегистрированных учеников.";
                                    $scope.model.modal_enroll.show_create_account = true;
                                    $scope.$apply();
                                }
                            } else {
                                $mdDialog.hide();
                                $scope.model.modal_enroll.show_error = false;
                                $scope.$apply();
                                $scope.load_course();
                            }
                        }, function(error) {
                            $scope.model.modal_enroll.show_error = true;
                            $scope.model.modal_enroll.error_message = "Invalid request";
                            $scope.$apply();
                            $log.error(error);
                        });
                    };

                    $scope.cancelCreateAccount = function($event) {
                        $scope.model.modal_enroll.show_create_account = false;
                        $scope.model.modal_enroll.inputed_address = null;
                        $scope.model.modal_enroll.error_message = null;
                        $scope.model.modal_enroll.show_error = false;
                    };

                    $scope.createAccount = function($event) {
                        var _data = {
                            lesson_id: $scope.assign_lesson_id,
                            email: $scope.model.modal_enroll.inputed_address
                        };

                        $.post('/api/create_pupil/', JSON.stringify(_data)).then(function(data) {
                            $scope.model.modal_enroll.show_create_account = false;
                            $scope.model.modal_enroll.inputed_address = null;
                            $scope.model.modal_enroll.error_message = null;
                            $scope.model.modal_enroll.show_error = false;

                            $mdDialog.hide();
                            $scope.load_course();
                        }, function(error) {
                            $scope.model.modal_enroll.show_error = true;
                            $scope.model.modal_enroll.error_message = "Invalid request";
                            $scope.$apply();
                            $log.error(error);
                        });
                    };
                }
            });
    };


    /*
    Удаление назначение на страницы курса
     */
    $scope.remove_enroll = function($event, enroll_id) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/confirm/confirm_delete_enroll.html',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function DialogController($scope, $mdDialog) {
                $scope.closeDialog = function() {
                    $mdDialog.hide();
                };

                $scope.submit = function() {
                    $mdDialog.hide();
                    $http.delete('/api/enroll/' + enroll_id + '/').then(function(data) {
                        $scope.load_course();
                    }, function(error) {
                        $log.error(error);
                    });
                };
            }
        });
    };


    $scope.play_lesson = function(enroll_id) {
        $location.path('/play/' + enroll_id + '/');
    };

    /**
     * Возвращает тип урока
     * @param  {[type]} lesson_id [description]
     * @return {[type]}           [description]
     */
    $scope.get_lesson_type = function(lesson_id) {
        var _lessons = $scope.model.course.lessons;
        for (var i = 0, len = _lessons.length; i < len; i++) {
            if (lesson_id == _lessons[i].id) {
                return _lessons[i].lesson_type;
            }
        }
    };


    // =============================
    $scope.load_course();


};

module.exports = ['$scope', '$mdDialog', '$http', '$log', '$location', '$stateParams', CourseCtrl];


