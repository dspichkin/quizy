'use strict';

var SignupCtrl = function($scope, $location, $log) {
    if ($scope.user && $scope.user.is_authenticated) {
        return $location.path('/accounts/profile');
    }

    // $scope.meta.is_login_close = false;

    $scope.submit = function($event) {
        $event.preventDefault();
        var form = $('form.signup');
        
        // console.log(form[0].csrfmiddlewaretoken.value, $cookies['csrftoken'], $http.defaults.headers.post['X-CSRFToken'] )
        // form[0].csrfmiddlewaretoken.value = $http.defaults.headers.post['X-CSRFToken'];

        $.post(form.attr('action'), form.serialize()).then(
            function(data) {
                if (data.csrf) {
                        $http.defaults.headers.post['X-CSRFToken'] = data.csrf;
                    }
                if (data.location) {
                    $scope.$apply(function() {
                        $location.path(data.location);
                    });

                }
            }, function(res) {
                //console.log(!!!, error)
                //$log.error(error)
                if (res.hasOwnProperty('responseText')) {
                    try {
                        var data = JSON.parse(res.responseText);
                        console.log('!', data.form_errors)
                        $scope.form_errors = data.form_errors;
                        $scope.$apply();
                    } catch (e) {
                        console.log(e)
                    }
                }
            });
    }
};

module.exports = ['$scope', '$location', '$log', SignupCtrl];



