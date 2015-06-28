'use strict';

var ProfileCtrl = function($scope, $http, $location, $log) {
    if (!$scope.user || !$scope.user.is_authenticated) {
        return $location.path('/');
    }

    $scope.model = {
        account_type: "Тип аккаунта",
        account_type_choice: ["Преподователь", "Студент"],
        show_pass_ok: false,
        error_msg: null

    };

    if ($scope.user.account_type == 1) {
        $scope.model.account_type = "Преподователь";
    } else {
        $scope.model.account_type = "Студент";
    }


    $scope.changePass = function() {
        if (typeof $scope.pass1 == 'undefined' || $scope.pass1 == "") {
            $scope.is_change_pass_error = true;
            $scope.model.error_msg = 'Пароль не может быть пустым';
            return;
        }

        if ($scope.pass1 != $scope.pass2) {
            $scope.is_change_pass_error = true;
            $scope.model.error_msg = 'Пароли не совпадают';
            return;
        }

        if ($scope.pass1 == $scope.pass2) {
            $scope.is_change_pass_error = false;
            $scope.save_pass();
        }
    };


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

    $scope.save_account_type = function() {
        var _at;
        if ($scope.model.account_type == "Преподователь") {
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
            },
            function(error) {
                $log.error(error);
            });
    };

    $scope.change_account_type = function() {
        if ($scope.user.account_type == 1 && $scope.model.account_type == "Студент") {
            $scope.user.account_type = 2;
            $scope.model.account_type = "Студент";
            $scope.save_account_type();
        }

        if ($scope.user.account_type == 2 && $scope.model.account_type == "Преподователь") {
            $scope.user.account_type = 1;
            $scope.model.account_type = "Преподователь";
            $scope.save_account_type();
        }
    };
};

module.exports = ['$scope', '$http', '$location', '$log', ProfileCtrl];