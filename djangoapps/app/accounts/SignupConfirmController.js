'use strict';

var SignupConfirmCtrl = function($scope, $stateParams, $http, $location, $state, $log) {
    if ($scope.user && $scope.user.is_authenticated) {
        return $location.path('/accounts/profile');
    }
    
    $scope.model = {
        show_loading: false,
        key: null,
        confirm: null,
        correct: false,
        user: null
    };
    if ($stateParams.hasOwnProperty('key')) {
        $http.get('/accounts/ajax-confirm-email/' + $stateParams.key + '/').then(
            function(data) {
                if (data.hasOwnProperty("data")) {
                    if (data.data.hasOwnProperty("key")) {
                        $scope.model.key = data.data.key;
                        $scope.model.correct = true;
                        $scope.model.user = data.data.user
                    }
                }
                console.log(data)
            },
            function(error) {
                $log.error('Ошибка проверки ключа подтверждения email', error);
            });
    }

    $scope.submit = function() {
        $scope.model.show_loading = true;
        if ($scope.model.key) {
            $http.post('/accounts/ajax-confirm-email/' + $scope.model.key + '/')
            .then(function() {
                $scope.model.show_loading = false;
                $location.path('/');
                 window.location.reload(); 
            }, function(error) {
                $scope.model.show_loading = false;
                $log.error('Ошибка проверки ключа подтверждения email', error);
            });
        }
    };
};

module.exports = ['$scope', '$stateParams', '$http', '$location', '$state', '$log', SignupConfirmCtrl];



