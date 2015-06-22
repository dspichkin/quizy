'use strict';

var SignupCtrl = function($scope, $location, $log) {
    if ($scope.user && $scope.user.is_authenticated) {
        return $location.path('/accounts/profile');
    }
    $scope.model = {
        show_loading: false,
        input_name: false,
        account_type: "Регистрировать как",
        account_type_choice: ["Учитель", "Ученик"]

    };

    // $scope.meta.is_login_close = false;

    $scope.submit = function($event) {
        $event.preventDefault();
        var form = $('form.signup');
        
        // console.log(form[0].csrfmiddlewaretoken.value, $cookies['csrftoken'], $http.defaults.headers.post['X-CSRFToken'] )
        // form[0].csrfmiddlewaretoken.value = $http.defaults.headers.post['X-CSRFToken'];
        var _at;
        if ($scope.model.account_type == "Учитель") {
            _at = 1;
        } else {
            _at = 2;
        }
        var _data = {
            "firstname": $("#id_firstname").val(),
            "secondname": $("#id_secondname").val(),
            "middle_name": $("#id_middle_name").val(),
            "email": $("#id_email").val(),
            "password1": $("#id_password1").val(),
            "password2": $("#id_password2").val(),
            "account_type": _at
        };
        $scope.model.show_loading = true;
        $.post(form.attr('action'), _data).then(
            function(data) {
                if (data.location) {
                    $scope.$apply(function() {
                        $scope.model.show_loading = false;
                        $location.path('/accounts/confirm-email/');
                    });

                }
            }, function(res) {
                $scope.model.show_loading = false;
                if (res.hasOwnProperty('responseText')) {
                    try {
                        var data = JSON.parse(res.responseText);
                        $scope.form_errors = data.form_errors;
                        $scope.$apply();
                    } catch (e) {
                        console.log(e)
                    }
                }
            });
    };

    $scope.close_modal = function(url) {
        $location.path(url);
    };

};

module.exports = ['$scope', '$location', '$log', SignupCtrl];



