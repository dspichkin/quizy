'use strict';

app.ControllerName = function($scope, $http, $log) {
    $scope.model['lesson_dialog'] = $scope.model.outside.enroll;
    $scope.model['lesson_dialog'].temptext = null;


    $scope.back_to_lessons = function() {
        $scope.main.go_courses_page($scope.model.outside.course_id);

    };

    $scope.get_answer_teacher = function() {
        if ($scope.model.lesson_dialog.data.steps.length > 0 && $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].type == 'pupil') {
            return true;
        }
    };

    $scope.add_answer_teacher = function() {
        $scope.model['lesson_dialog'].temptext = null;
        $scope.model.lesson_dialog.data.steps.push({
            number: $scope.model.lesson_dialog.data.steps.length + 1,
            type: "teacher",
            text: "",
            mode: 'edit'
        });
    };

    $scope.get_step_by_number = function(number, data) {
        for (var i = 0, len = $scope.model.lesson_dialog.data.steps.length; i < len; i++) {
            if ($scope.model.lesson_dialog.data.steps[i].number == number) {
                if (data.hasOwnProperty('text')) {
                    $scope.model.lesson_dialog.data.steps[i].text = data.text;
                }
                if (data.hasOwnProperty('mode')) {
                    $scope.model.lesson_dialog.data.steps[i].mode = data.mode;
                }
                return $scope.model.lesson_dialog.data.steps[i];
            }
        }
    };

    $scope.edit_step = function(number) {
        var step = $scope.get_step_by_number(number, {
            mode: 'edit'
        });
        $scope.model.lesson_dialog.temptext = step.text;
    };

    $scope.delete_step = function(number) {
        var index = null;
        for (var i = 0, len = $scope.model.lesson_dialog.data.steps.length; i < len; i++) {
            if ($scope.model.lesson_dialog.data.steps[i].number == number) {
                index = i;
                break;
            }
        }
        if (index != null) {
            $scope.model.lesson_dialog.data.steps.splice(index, 1);
            $scope.save();
        }
    };


    $scope.save_step = function(number) {
        $scope.get_step_by_number(number, {
            text: $scope.model.lesson_dialog.temptext,
            mode: null
        });

        $scope.save();
    };



    $scope.save = function() {
        var _data = $scope.model.lesson_dialog.data;
        $http.put('/api/enroll_teacher/' + $scope.model.lesson_dialog.id + '/', JSON.stringify(_data))
            .then(function() {}, function(error) {
                $log.error(error);
            });
    } 

}