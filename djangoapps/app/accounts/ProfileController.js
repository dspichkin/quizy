'use strict';

var ProfileCtrl = function($scope, $location) {
    if ($scope.user.first_name || $scope.user.last_name) {
        if (!$scope.user.first_name) {
            $scope.user_name = $scope.user.last_name;
        }
        if (!$scope.user.last_name) {
            $scope.user_name = $scope.user.first_name;
        } else {
            $scope.user_name = $scope.user.first_name + " " + $scope.user.last_name;
        }
    } else {
        if ($scope.username) $scope.user_name = $scope.username.split('@')[0]; //
    }
    if (!$scope.user || !$scope.user.is_authenticated) {
        return $location.path('/');
    }
    $scope.changePass = function() {
        if ($scope.pass1 != $scope.pass2) $scope.is_change_pass_error = true;
    };
    //$scope.cleanupDom();
};

module.exports = [ '$scope', '$location', ProfileCtrl ];