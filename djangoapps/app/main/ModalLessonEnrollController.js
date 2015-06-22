'use strict';

var ModalInstanceLessonEnrollCtrl = function($scope, $modalInstance, $log, lesson_id) {
    $scope.model = {
        show_user: true,
        inputed_address: "",
        show_invite: false
    }

    $scope.ok = function() {
        //$modalInstance.close($scope.selected.item);
        if ($scope.model.show_user == true) {
            var _data = {
                lesson_id: lesson_id,
                email: $scope.model.inputed_address
            };
            $.post('/api/set_enroll_user/', _data).then(function(data) {
                if (data.hasOwnProperty('signal')) {
                    if (data.signal == 'invite') {
                        $scope.model.show_user = false;
                        $scope.model.show_invite = true;
                        $scope.$apply();
                    }
                }
                if (data.hasOwnProperty('code')) {
                    if (data.code == 200) {
                        $modalInstance.close();
                    }
                }
                if (data.hasOwnProperty('code')) {
                    if (data.code == 300) {
                        $scope.model.show_user = false;
                        $scope.model.show_invite = false;
                        $scope.model.show_error = true;
                        $scope.model.error_message = "Не верный email"
                        $scope.$apply();
                    }
                }
            }, function(error) {
                $log.error(error);
            });
        }

        if ($scope.model.show_invite == true) {
            $scope.model.show_user = true;
            $scope.model.show_invite = false;
        }

        if ($scope.model.show_error == true) {
            $scope.model.show_user = true;
            $scope.model.show_invite = false;
            $scope.model.show_error = false;
        }

    };

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };
}


module.exports = ['$scope', '$modalInstance', '$log', 'lesson_id', ModalInstanceLessonEnrollCtrl];