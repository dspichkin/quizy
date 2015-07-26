'use strict';
var MainCtrl = function($scope, $state, $sce, $http, $mdDialog, $location, $timeout, $log) {
    $scope.user = {
        username: 'guest',
        is_authenticated: false,
        loaded: false
    };

    window.scope = $scope;

    // высота окна сообщения
    var message_height = 48;
    // высота короткой шапки
    var short_header_height = 150;

    var t = '<button class="md-raised pull-right md-button md-default-theme" ng-transclude="" ng-click="new_lesson()" style="background-color: #FF9E37;    margin: -8px 43px 0 0px;" tabindex="0"><span class="ng-scope">Обработать заявки</span><div class="md-ripple-container"></div></button>';
    $scope.model = {
        selected_menu: null,
        menu: {
            positionTop: '0px',
            positionLoginTextTop: '0px',
            positionBodyTop: '0px', // позиция страницы
            positionMainMenuLeft: '0px', // позиция главного меню
            positionMainMenuTop: '252px', // позиция главного меню
            positionTitleLeft: '-4px', // позиция названия
            positionTitleTop: '68px' // позиция названия
        },
        message: {
            is_active: false,
            current_message: 0,
            text: [$sce.trustAsHtml('Message from server <b>ddd</b> ' + t)],
            next_message: function() {
                $scope.model.message.current_message += 1;
                if ($scope.model.message.current_message >= $scope.model.message.text.length) {
                    $scope.model.message.current_message = 0;
                }
            }
        }
    };


    $scope.main = {
        active_menu: 'main',
        current_course: null
    };

    $scope.main.reset_menu = function() {
        if ($scope.model.message.is_active == true) {
            $scope.model.menu.positionTop = message_height + 'px';
            $scope.model.menu.positionBodyTop = (300 + message_height) + 'px';
        } else {
            $scope.model.menu.positionTop = '0px';
            $scope.model.menu.positionBodyTop = '300px';
            $scope.model.menu.positionMainMenuLeft = '0px';
            $scope.model.menu.positionMainMenuTop = '252px';
            $scope.model.menu.positionTitleLeft = '-4px';
            $scope.model.menu.positionTitleTop = '68px';
        }
        $scope.model.menu.positionLoginTextTop = '0px';

        $scope.main.active_menu = 'main';
    };

    $scope.main.make_short_header = function() {
        if ($scope.model.message.is_active == true) {
            $scope.model.menu.positionTop = (-short_header_height + message_height) + 'px';
            $scope.model.menu.positionBodyTop = (short_header_height + message_height) + 'px';
        } else {
            $scope.model.menu.positionTop = -short_header_height + 'px';
            $scope.model.menu.positionBodyTop = short_header_height + 'px';

            $scope.model.menu.positionMainMenuTop = '180px';
            $scope.model.menu.positionTitleLeft = '37%';
            $scope.model.menu.positionTitleTop = '180px';
            $scope.model.menu.positionMainMenuLeft = '5%';
        }
        $scope.model.menu.positionLoginTextTop = short_header_height + 'px';

        window.scrollTo(0, 0);
    };

    $scope.main.reset_menu();

    $scope.main.go_home_page = function() {
        $location.path('/');
        //$scope.model.current_content_url = 'assets/partials/main.html';
        $scope.main.reset_menu();
        $scope.main.run();

        $scope.main.active_menu = 'main';
    };



    $scope.main.go_courses_page = function(course_id) {
        if (course_id) {
            $location.path('/courses/' + course_id + '/');
        } else {
            $location.path('/courses/');
        }
        $scope.main.make_short_header();
        $scope.main.active_menu = 'courses';
    };

    $scope.main.go_lesson_page = function() {
        $location.path('/lessons/');
        $scope.main.make_short_header();
        $scope.main.active_menu = 'lessons';
    };

    $scope.main.go_price = function() {
        $scope.main.reset_menu();
        $scope.main.active_menu = 'price';
        $location.path('/price/');
    };

    $scope.main.go_description = function() {
        $location.path('/');
        $scope.main.active_menu = 'description';
        $scope.main.reset_menu();
    };

    $scope.main.go_pupils_page = function() {
        $location.path('/pupils/');
        $scope.main.active_menu = 'pupils';
    };

    $scope.main.new_lesson = function(course) {
        $scope.main.current_course = course;
        $location.path('/editor/lesson/');
        $scope.model.current_content_url = null;
        $scope.main.make_short_header();
        $scope.main.active_menu = 'lessons';
    };

    $scope.main.go_editor_lesson = function(lesson_id) {
        if (lesson_id) {
            $location.path('/editor/lesson/' + lesson_id + '/');
        } else {
            $location.path('/editor/lesson/');
        }
        $scope.main.make_short_header();
        $scope.main.active_menu = 'lessons';
    };

    $scope.main.go_play = function(enroll_id) {
        if (lesson_id) {
            $location.path('/play/' + enroll_id + '/');
            $scope.main.make_short_header();
            $scope.main.active_menu = 'lessons';
        }
    };

    $scope.main.go_test_play = function(lesson_id) {
        if (lesson_id) {
            $location.path('/play/demo/' + lesson_id + '/');
            $scope.main.make_short_header();
            $scope.main.active_menu = 'lessons';
        }
    };


    $scope.main.go_profile = function() {
        $location.path('/accounts/profile/');
        $scope.main.make_short_header();
        $scope.main.active_menu = 'profile';
    };



    $scope.main.run = function(callback) {
        var config = {
            headers: {
                'Accept': 'application/json; indent=4'
            }
        };

        $.ajax({
            type: "GET",
            url: '/api/user/',
            async: false
        }).then(function(data) {
            $scope.user = data;
            $scope.user.loaded = true;

            if (callback) {
                callback();
            }
        }, function(error) {
            $log.error('Ошибка получения данных', error);
            if (callback) {
                callback();
            }
        });
        
        /*
        var userget = $http.get('/api/user/', config).then(function(data) {
            $scope.user = data.data;
            $scope.user.loaded = true;

            if (callback) {
                callback();
            }
        }, function(error) {
            if (callback) {
                callback();
            }
            $log.error('Ошибка получения данных', error);
        });
        //return userget;
        */

    };

    $scope.main.login = function($event) {
        if ($event) {
            $event.preventDefault();
        }
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/login.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {

                    $scope.model.login = {
                        email: '',
                        password: '',
                        form_errors: {},
                        loading: false,
                        show_recall: false
                    };
                    $scope.form_errors = {};
                    $scope.closeDialog = function($event) {
                        $mdDialog.hide();
                    };

                    $scope.show_recall = function($event) {
                        $event.preventDefault();
                        $scope.model.login.show_recall = true;
                    };

                    $scope.recall = function($event) {
                        $event.preventDefault();
                        $scope.model.login.show_recall = true;
                        $scope.model.login.loading = true;

                        var _data = {
                            'email': $scope.model.login.email
                        };
                        

                        $.post('/accounts/ajax-recall/', JSON.stringify(_data)).then(
                            function(data) {
                                $scope.model.login.email = null;
                                $scope.model.login.loading = false;
                                console.log(data)
                                if (data.hasOwnProperty('form_errors')) {
                                    if (data.form_errors) {
                                        $scope.model.login.form_errors = data.form_errors;
                                        $scope.$apply();
                                        return;
                                    }
                                } else {
                                    $location.path('/');
                                    $scope.main.run(function() {
                                        $mdDialog.hide()
                                    });
                                }
                            }, function(e) {
                                $scope.model.login.email = null;
                                $scope.user.loaded = true;
                                $log.error(e);
                            }
                        );
                    }

                    $scope.cancel_recall = function($event) {
                        $event.preventDefault();
                        $scope.model.login.show_recall = false;
                    }

                    $scope.submit = function($event) {
                        $event.preventDefault();
                        $scope.model.login.loading = true;
                        $scope.user.loaded = false;
                        var _data = {
                            'email': $scope.model.login.email,
                            'password': $scope.model.login.password
                        };
                        $.post('/accounts/ajax-login/', JSON.stringify(_data)).then(
                            function(data) {
                                $scope.model.login.loading = false;
                                if (data.hasOwnProperty('form_errors')) {
                                    if (data.form_errors) {
                                        $scope.model.login.form_errors = data.form_errors;
                                        $scope.$apply();
                                        return;
                                    }
                                } else {
                                    $location.path('/');
                                    $scope.main.run(function() {
                                        $mdDialog.hide()
                                    });
                                }
                            }, function(e) {
                                $scope.user.loaded = true;
                                $log.error(e);
                            }
                        );
                    };
                }
            });
    };





    $scope.main.logout = function($event) {
        if ($event) {
            $event.preventDefault();
        }
        $scope.user.loaded = false;
        $http.post('/accounts/ajax-logout/').then(function(data) {
            $scope.main.go_home_page();
        }, function(error) {
            $log.error('Ошибка выхода', error);
        });
    };



    //===================================

    $scope.main.run();
};


module.exports = ['$scope', '$state', '$sce', '$http', '$mdDialog', '$location', '$timeout', '$log', MainCtrl];

