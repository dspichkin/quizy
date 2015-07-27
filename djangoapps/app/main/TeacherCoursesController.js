'use strict';
function getUrlVars(url)
{
    var vars = [], hash;
    var hashes = url.slice(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}


var _ = require('lodash-node');
var Course = require('../models/course');
var CoursesCtrl = function($scope, $stateParams, $mdDialog, $http, $data, $timeout, $log, $location) {
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


    $scope.load_courses = function(url, callback) {
        if ($scope.user.account_type == 1) {
            var _page;
            if (!url) {
                var url = '/api/courses/';
                if (_page) {
                    url += '?page=' + _page;
                }
            } else {
                _page = getUrlVars(url).page;
            }
            if (!_page) {
                _page = 1;
            }


            $http.get(url).then(function(data) {
                $scope.model.courses = [];
                var page_length = 10;
                for (var i = 0, len = data.data.results.length; i < len; i++) {
                    $scope.model.courses.push(new Course(data.data.results[i]));
                }
                var from_page = _page * page_length - page_length;
                if (!from_page) {
                    from_page = 1;
                }
                var to_page = _page * page_length;
                if (to_page > data.data.count) {
                    to_page = data.data.count;
                }
                $scope.model.page = {
                    next: data.data.next,
                    count: data.data.count,
                    previous: data.data.previous,
                    from_page: from_page,
                    to_page: to_page
                };

            }, function(error) {
                $log.error('Ошибка получения курсов', error);
            });
        }
    };

    $scope.go_page = function(url) {
        $location.path(url);
    };

    $scope.go_course_lessons = function(course_id) {
        $location.path('/courses/' + course_id + '/');
    };

    $scope.course_enroll = function($event, course_id) {

        $scope.assign_course_id = course_id;
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/partials/courses/assign_course.html',
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

module.exports = ['$scope', '$stateParams', '$mdDialog', '$http', '$data', '$timeout', '$log', '$location', CoursesCtrl];


