'use strict';
var MainCtrl = function($scope, $http, $cookies, $location, $state, $timeout, $log) {
    $scope.user = {
        username: 'guest',
        is_authenticated: false,
        loaded: false
    };
    $scope.course = null;
    $scope.content = null;
    $scope.meta = {};
    $scope.meta.is_short_menu = null;

    $scope.getMainScope = function() {
        return $scope;
    };


    $scope.apiErrorHandler = function() {
        alert('Сервер не отвечает');
    };



    $scope.updateData = function(callback) {
        var config = {
            headers: {
                'Accept': 'application/json; indent=4'
            }
        };


        var userget = $http.get('/api/user/', config).then(function(data) {
            $scope.user = data.data;
            $scope.user.loaded = true;

            if (!$scope.user.is_authenticated) {
                $scope.my_lessons = null;
                if (callback) callback();
                return;
            }
            /*
            $http.get('/api/lessons/', config).then(function(data) {
                $scope.my_lessons = data.data;
                if (callback) callback();
            }, function(error) {
                $log.error('Ошибка получения уроков', error);
            });
            */

        }, function(error) {
            $log.error('Ошибка получения данных', error);
        });
        return userget;

    };
    

    $scope.logout = function($event) {
        if ($event) {
            $event.preventDefault();
        }
        $http.post('/accounts/ajax-logout/').success(function(data) {
            if (data.csrf) {
                $http.defaults.headers.post['X-CSRFToken'] = data.csrf;
            }
            // Сбросим все текущие данные
            $scope.user = {
                username: 'guest',
                is_authenticated: false,
                loaded: false
            };
            $scope.content = null;
            $scope.course = null;
            $scope.updateData(function() {
                $location.path('/');
            })
        }).error($scope.apiErrorHandler);
    };
    
    
    /*
    $scope.notAuthGoTo = function(state) {
        $scope.meta.is_login_close = true;
        $timeout(function() {
            $state.go(state);
        }, 1000);
    };
    
    $scope.toggleMenu = function($event, screen, is_mobile_toggle) {
        if ($event) $event.preventDefault();
        if (window.innerWidth > 480 && !is_mobile_toggle) {
            // переключение на desktop
            if (screen) {
                // клик на пункте меню
                if ($scope.meta.is_short_menu) {
                    // если меню свернуто,то разворачвиаем
                    $scope.meta.is_short_menu = false;
                } else if ($state.current.name == screen) {
                    // если меню развернуто и мы кликаем на активный пункт
                    $scope.meta.is_short_menu = true;
                }
            } else {
                // клик на переключатель вида меню
                $scope.meta.is_short_menu ? $scope.meta.is_short_menu = false : $scope.meta.is_short_menu = true;
            }
        } else {
            // переключение на мобильных устройствах
            if (!screen) {
                if ($scope.meta.is_lesson_screen) {
                    $scope.meta.is_lesson_screen = false;
                } else {
                    if ($scope.meta.is_add_user_screen) {
                        $scope.meta.is_add_user_screen = false;
                    } else {
                        $scope.meta.is_lesson_screen = true;
                    }
                }
            }
        }
    };
    */
    //===================================

    $scope.updateData();
};


module.exports = ['$scope', '$http', '$cookies', '$location', '$state', '$timeout', '$log', MainCtrl];

