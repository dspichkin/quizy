'use strict';

var ProfileCtrl = function($scope, $http, $location, $log,  $mdDialog) {
    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.reset_menu();
        $location.path('/');
        return;
    }

    $scope.main.make_short_header();
    $scope.main.active_menu = 'profile';


    $scope.model['profile'] = {
        is_dirty_data: false,
        account_type: "Тип аккаунта",
        account_type_choice: ["Преподователь", "Студент"],
        show_pass_ok: false,
        error_msg: null,
        user: $scope.user
    };


    if ($scope.user.account_type == 1) {
        $scope.model.profile.account_type = "Преподователь";
    } else {
        $scope.model.profile.account_type = "Студент";
    }


    $scope.changePass = function(callback) {
        if (typeof $scope.model.profile.pass1 == 'undefined' || $scope.model.profile.pass2 == "") {
            $scope.model.profile.error_msg = 'Пароль не может быть пустым';
            return;
        }

        if ($scope.model.profile.pass1 != $scope.model.profile.pass2) {
            $scope.model.profile.error_msg = 'Пароли не совпадают';
            return;
        }

        if ($scope.model.profile.pass1 == $scope.model.profile.pass2) {
            $scope.model.profile.error_msg = null;
            $scope.model.profile.user.password = $scope.model.profile.pass1;
            $scope.save_account();
            if (callback) {
                callback();
            }
        }
    };

    /*
    $scope.save_pass = function() {
        var _data = {
            password: $scope.pass1
        };
        $http.post('/accounts/ajax-profile/', JSON.stringify(_data)).then(
            function(data) {
                $scope.user = data.data;
                $scope.model.show_pass_ok = true;
                $scope.is_show_pass = false;
            },
            function(error) {
                $log.error(error);
            });
    };
    */

    $scope.change_password = function($event) {
        $mdDialog.show({
              targetEvent: $event,
              templateUrl: '/assets/partials/change_password.html',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function DialogController($scope, $mdDialog) {

                    $scope.form_errors = {};
                    $scope.closeDialog = function() {
                        $mdDialog.hide();
                    };
                    $scope.submit = function($event) {
                        $event.preventDefault();
                        $scope.changePass(function() {$mdDialog.hide()});
                    };
                }
        });
    }

    $scope.save_account_type = function() {
        var _at;
        if ($scope.model.profile.account_type == "Преподователь") {
            _at = 1;
        } else {
            _at = 2;
        }
        var _data = {
            account_type: _at
        };
        $http.post('/accounts/ajax-profile/', JSON.stringify(_data)).then(
            function(data) {
                $scope.user = data.data;
                $scope.model.profile.is_dirty_data = false;
            },
            function(error) {
                $log.error(error);
            }
        );
    };
   
    $scope.save_account = function() {
        $http.post('/accounts/ajax-profile/', JSON.stringify($scope.model.profile.user)).then(
            function(data) {
                $scope.user = data.data;
                $scope.model.profile.is_dirty_data = false;
            },
            function(error) {
                $log.error(error);
            }
        );
    }

    $scope.make_data_dirty = function() {
        $scope.model.profile.is_dirty_data = true;
    };


};

module.exports = ['$scope', '$http', '$location', '$log', '$mdDialog', ProfileCtrl];