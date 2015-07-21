'use strict';

var _ = require('lodash-node');
var Lesson = require('../models/lesson');
var Course = require('../models/course');

var LessonsCtrl = function($scope, $mdDialog, $http, $data, $timeout, $log, $location, $filter, ngTableParams) {
    $scope.model = {
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


    

    var data = [{name: "Moroni", age: 50, role: 'Administrator'},
            {name: "Tiancum", age: 43, role: 'Administrator'},
            {name: "Jacob", age: 27, role: 'Administrator'},
            {name: "Nephi", age: 29, role: 'Moderator'},
            {name: "Enos", age: 34, role: 'User'},
            {name: "Tiancum", age: 43, role: 'User 1'},
            {name: "Jacob", age: 27, role: 'User 1'},
            {name: "Nephi", age: 29, role: 'Moderator'},
            {name: "Enos", age: 34, role: 'User 1'},
            {name: "Tiancum", age: 43, role: 'Moderator'},
            {name: "Jacob", age: 27, role: 'User'},
            {name: "Nephi", age: 29, role: 'User'},
            {name: "Enos", age: 34, role: 'Moderator'},
            {name: "Tiancum", age: 43, role: 'User'},
            {name: "Jacob", age: 27, role: 'User'},
            {name: "Nephi", age: 29, role: 'User'},
            {name: "Enos", age: 34, role: 'User'}];

            /*
    $scope.tableParams = new ngTableParams({
            page: 1,            // show first page
            count: 10          // count per page
        }, {
            groupBy: 'role',
            total: data.length,
            getData: function($defer, params) {
                var orderedData = params.sorting() ?
                        $filter('orderBy')(data, $scope.tableParams.orderBy()) :
                        data;

                $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
            }
        });
*/





    $scope.load_lesson = function(callback) {
        if ($scope.user.account_type == 1) {
            $http.get('/api/lessons/').then(function(data) {
                $scope.model.lessons = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    $scope.model.lessons.push(new Lesson(data.data[i]));
                }


                console.log("!", $scope.model.lessons)

                $scope.tableParams = new ngTableParams({
                    page: 1,            // show first page
                    count: 10          // count per page
                }, {
                    groupBy: 'course',
                    total: $scope.model.lessons,
                    getData: function($defer, params) {
                        var orderedData = params.sorting() ?
                                $filter('orderBy')($scope.model.lessons, $scope.tableParams.orderBy()) :
                                $scope.model.lessons;

                        $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
                    }
                });



                /*
                $http.get('/api/archive/').then(function(data) {
                    $scope.model.lesson.archive = [];
                    for (var i = 0, len = data.data.length; i < len; i++) {
                        var l = new Lesson(data.data[i]);
                        $scope.model.lesson.archive.push(l);
                    }

                    setTimeout(function() {
                        $scope.$apply();
                    });
                    if (callback) {
                        callback();
                    }
                }, function(error) {
                    $log.error('Ошибка получения архива уроков', error);
                });
                */
            }, function(error) {
                $log.error('Ошибка получения уроков', error);
            });
        } else {
            $http.get('/api/mylessons/').then(function(data) {
                $scope.model.lesson.lessons_for_me = [];
                for (var i = 0, len = data.data.length; i < len; i++) {
                    data.data[i].created_at = Date.parse(data.data[i].created_at);
                    $scope.model.lesson.lessons_for_me.push(data.data[i]);
                }
            }, function(error) {
                $log.error('Ошибка получения назначенных на меня уроков', error);
            });
        }
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

    $scope.main.new_lesson = function() {
        $scope.main.go_editor_lesson();
    };


    $scope.remove_enroll = function(enroll_id) {
        $http.delete('/api/enroll_pupil/' + enroll_id + '/').then(function(data) {
            $scope.load_lesson();
        }, function(error) {
            $log.error(error);
        });
    };



    $scope.play_lesson = function(enroll_id) {
        $location.path('/play/' + enroll_id + '/');
    };

    $scope.move_to_archive = function(lesson_id) {
        $http.post('/api/archive/' + lesson_id + "/").then(function(data) {
            $scope.load_lesson();
        }, function(error) {
            $log.error('Ошибка перемещения урока в архив', error);
        });
    };


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
                    $scope.submit_disabled = true;
                    $scope.change_inputed_address = function() {
                        if ($scope.model.modal_find_teacher.inputed_address != "") {
                            $scope.submit_disabled = false;
                        } else {
                            $scope.submit_disabled = true;
                        }
                    }
                    $scope.ok = function($event) {
                        var _data = {
                            email: $scope.model.modal_find_teacher.inputed_address
                        };

                        $scope.model.modal_find_teacher.loading = true;
                        $.get('/api/find_teacher/', _data).then(function(data) {
                            $scope.model.modal_find_teacher.loading = false;
                            if (data.hasOwnProperty('code')) {
                                if (data.code == 200) {
                                    $mdDialog.hide();
                                    $scope.model.modal_find_teacher.show_error = false;
                                    $mdDialog.hide();
                                }
                            } 
                            $scope.model.modal_find_teacher.show_error = true;
                            $scope.model.modal_find_teacher.error_message = "Указаный вами email " +
                                $scope.model.modal_find_teacher.inputed_address + " не найден среди зарегистрированных преподователей.";
                            $scope.$apply();

                        }, function(error) {
                            $scope.model.modal_find_teacher.show_error = true;
                            $scope.model.modal_find_teacher.error_message = "Invalid request";
                            $scope.$apply();
                            $log.error(error);
                        });

                    };
                }
            });
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

                    $scope.get_mypupils = function() {
                        $.get('/api/get_mypupil/').then(function(data) {
                            $scope.model.modal_enroll.mypupils = data;
                            $scope.$apply();
                        }, 
                        function(error) {
                            $scope.model.modal_enroll.show_error = true;
                            $scope.model.modal_enroll.error_message = "Invalid request";
                            $scope.$apply();
                            $log.error(error);
                        });
                    }

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
                            lesson_id: $scope.assign_lesson_id,
                            email: $scope.model.modal_enroll.inputed_address
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
                                    $scope.$apply();
                                }
                            } else {
                                $mdDialog.hide();
                                $scope.model.modal_enroll.show_error = false;
                                $scope.$apply();
                                $scope.load_lesson();
                            }
                        }, function(error) {
                            $scope.model.modal_enroll.show_error = true;
                            $scope.model.modal_enroll.error_message = "Invalid request";
                            $scope.$apply();
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
                            lesson_id: $scope.assign_lesson_id,
                            email: $scope.model.modal_enroll.inputed_address
                        };

                        $.post('/api/create_pupil/', JSON.stringify(_data)).then(function(data) {
                            $scope.model.modal_enroll.show_create_account = false;
                            $scope.model.modal_enroll.inputed_address = null;
                            $scope.model.modal_enroll.error_message = null;
                            $scope.model.modal_enroll.show_error = false;

                            $mdDialog.hide();
                            $scope.load_lesson();
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


    // =============================
    $scope.load_lesson();


};

module.exports = ['$scope', '$mdDialog', '$http', '$data', '$timeout', '$log', '$location', '$filter', 'ngTableParams', LessonsCtrl];


