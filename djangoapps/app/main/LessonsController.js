'use strict';

var _ = require('lodash-node');
var Lesson = require('../models/lesson');

var LessonsCtrl = function($scope, $mdDialog, $http, $data, $timeout, $log, $location) {
    $scope.model.lesson = {
        lessons: [],
        lessons_for_me: [],
        archive: [],
        show_user: true,
        inputed_address: "",
        show_invite: false,

        fabAction: {
            isOpen: false,
            selectedMode: 'md-fling',
            selectedDirection: 'right'
        }

    };

    if (!$scope.user || !$scope.user.is_authenticated) {
        $location.path('/');
    }


    $scope.main.go_lessons_page();

    $scope.load_lesson = function(callback) {
        $http.get('/api/mylessons/').then(function(data) {
            $scope.model.lesson.lessons_for_me = [];
            for (var i = 0, len = data.data.length; i < len; i++) {
                var l = new Lesson(data.data[i]);
                $scope.model.lesson.lessons_for_me.push(l);
            }
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });

        $http.get('/api/lessons/').then(function(data) {
            $scope.model.lesson.lessons = [];
            for (var i = 0, len = data.data.length; i < len; i++) {
                var l = new Lesson(data.data[i]);
                $scope.model.lesson.lessons.push(l);
            }
            $http.get('/api/archive/').then(function(data) {
                $scope.model.lesson.archive = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    var l = new Lesson(data.data[i]);
                    $scope.model.lesson.archive.push(l);
                }
                setTimeout(function() {
                    $scope.$apply();
                })
                if (callback) {
                    callback();
                }
            }, function(error) {
                $log.error('Ошибка получения архива уроков', error);
            });
        }, function(error) {
            $log.error('Ошибка получения уроков', error);
        });

        
    };

    $scope.delete_lesson = function(lesson_id) {
        var _index = -1;
        for (var i = 0, len = $scope.model.lesson.lessons.length; i < len; i++) {
            if ($scope.model.lesson.lessons[i].id == lesson_id) {
                _index = i;
                break;
            }
        }

        if (_index > -1) {
            $scope.model.lesson.lessons[_index].remove().then(function() {
                $scope.model.lesson.lessons.splice(_index, 1);
                $scope.$apply();
            }, function() {
                $log.error("Ошибка удаления урока.", error);
            });
        }
    };

    $scope.edit_lesson = function(lesson_id) {
        $location.path('/editor/' + lesson_id + '/');
    };

    $scope.main.new_lesson = function() {
        //$location.path('/editor/');
        $scope.main.go_editor_lesson()
    };

    $scope.play_lesson = function(lesson_id) {
        $location.path('/play/' + lesson_id + '/');
    };

    $scope.lesson_enroll = function($event, lesson_id) {
        $scope.model.assign_lesson_id = lesson_id;
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/assign_lesson.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {
                    $scope.model['modal_enroll'] = {
                        show_user: true,
                        inputed_address: "",
                        show_error: false,
                        error_message: ""
                    };
                    $scope.form_errors = {};
                    $scope.closeDialog = function() {
                        $mdDialog.hide();
                    };
                    $scope.ok = function($event) {
                        var _data = {
                            lesson_id: $scope.model.assign_lesson_id,
                            email: $scope.model.modal_enroll.inputed_address
                        };
                        $scope.model.modal_enroll.loading = true;
                        $.post('/api/enroll_user/', _data).then(function(data) {
                            $scope.model.modal_enroll.loading = false;
                            if (data.hasOwnProperty('signal')) {
                                if (data.signal == 'invite') {
                                    $scope.model.modal_enroll.show_user = false;
                                    $scope.model.modal_enroll.show_invite = true;
                                    $scope.$apply();
                                }
                            }
                            if (data.hasOwnProperty('code')) {
                                if (data.code == 200) {
                                    $mdDialog.hide();
                                    $scope.model.modal_enroll.show_error = false;
                                    $scope.$apply();
                                    $scope.load_lesson();
                                }
                            }
                            if (data.hasOwnProperty('code')) {
                                if (data.code == 300) {
                                    $scope.model.modal_enroll.show_error = true;
                                    $scope.model.modal_enroll.error_message = "Указаный вами email " +
                                        $scope.model.modal_enroll.inputed_address + " не найден среди зарегистрированных пользователей.";
                                    $scope.$apply();
                                }
                            }
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

    $scope.remove_enroll = function(enroll_id) {
        $http.delete('/api/enroll_user/' + enroll_id + '/').then(function(data) {
            $scope.load_lesson();
        }, function(error) {
            $log.error(error);
        });
    };


    $scope.play_lesson = function(lesson_id) {
        $location.path('/play/' + lesson_id + '/');
    }

    $scope.move_to_archive = function(lesson_id) {
        $http.post('/api/archive/' + lesson_id + "/").then(function(data) {
            $scope.load_lesson();
        }, function(error) {
            $log.error('Ошибка перемещения урока в архив', error);
        });
    }


    $scope.find_teacher = function($event) {
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/find_teacher.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {
                    $scope.model['modal_find_teacher'] = {
                        show_user: true,
                        inputed_address: "",
                        show_error: false,
                        error_message: ""
                    };
                    $scope.form_errors = {};
                    $scope.closeDialog = function() {
                        $mdDialog.hide();
                    };
                    $scope.ok = function($event) {
                        var _data = {
                            teacher_id: ""
                        };
                        $scope.model.modal_find_teacher.loading = true;
                        $.post('/api/enroll_user/', _data).then(function(data) {
                            $scope.model.modal_find_teacher.loading = false;
                            
                            if (data.hasOwnProperty('code')) {
                                if (data.code == 200) {
                                    $mdDialog.hide();
                                    $scope.model.modal_find_teacher.show_error = false;
                                    $scope.$apply();
                                    $scope.load_lesson();
                                }
                            }
                            if (data.hasOwnProperty('code')) {
                                if (data.code == 300) {
                                    $scope.model.modal_find_teacher.show_error = true;
                                    $scope.model.modal_find_teacher.error_message = "Указаный вами email " +
                                        $scope.model.modal_find_teacher.inputed_address + " не найден среди зарегистрированных пользователей.";
                                    $scope.$apply();
                                }
                            }
                        }, function(error) {
                            $scope.model.modal_find_teacher.show_error = true;
                            $scope.model.modal_find_teacher.error_message = "Invalid request";
                            $scope.$apply();
                            $log.error(error);
                        });
                    };
                }
            });
        
    }

    // =============================
    $scope.load_lesson()


};

module.exports = ['$scope', '$mdDialog', '$http', '$data', '$timeout', '$log', '$location', LessonsCtrl];