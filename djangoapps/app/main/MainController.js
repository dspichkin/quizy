'use strict';
var MainCtrl = function($scope, $http, $mdDialog, $location, $timeout, $log) {
    $scope.user = {
        username: 'guest',
        is_authenticated: false,
        loaded: false
    };
    $scope.model = {
        selected_menu: null,
        current_content_url: 'assets/partials/main.html',
        menu: {
            positionTop: 0,
            positionLoginTop: 0
        }
    };
    $scope.main = {};

    var reset_menu = function() {
        $scope.model.menu.positionTop = '0px';
        $scope.model.menu.positionLoginTop = '0px';
    }

    $scope.main.go_home_page = function() {
        $location.path('/');
        $scope.model.current_content_url = 'assets/partials/main.html';
        reset_menu();
        $scope.run();
    };

    $scope.main.go_lesson_page = function() {
        $location.path('/lessons/');
        $scope.model.current_content_url = null;
        $scope.model.menu.positionTop = '-252px';
        $scope.model.menu.positionLoginTop = '252px';
        window.scrollTo(0, 0);
       console.log(window.pageYOffset)
    };

    $scope.main.go_price = function() {
        $location.path('/');
        $scope.model.current_content_url = 'assets/partials/price.html';
        reset_menu();
    };

    $scope.main.go_description = function() {
        $location.path('/');
        $scope.model.current_content_url = 'assets/partials/help.html';
        reset_menu();
    };



    $scope.main.run = function(callback) {
        var config = {
            headers: {
                'Accept': 'application/json; indent=4'
            }
        };

        var userget = $http.get('/api/user/', config).then(function(data) {
            $scope.user = data.data;
            $scope.user.loaded = true;
            setTimeout(function() {
                $scope.$apply();
            });

            if (callback) {
                callback();
            }
        }, function(error) {
            if (callback) {
                callback();
            }
            $log.error('Ошибка получения данных', error);
        });
        return userget;

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
                        loading: false
                    };
                    $scope.form_errors = {};
                    $scope.closeDialog = function() {
                        $mdDialog.hide();
                    };
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
                                $log.error(e)
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
            $location.path('/');
            $scope.main.run();
        }, function(error) {
            $log.error('Ошибка выхода', error);
        })
    };


    //===================================

    $scope.main.run();
};


module.exports = ['$scope', '$http', '$mdDialog', '$location', '$timeout', '$log', MainCtrl];

