'use strict';

app.ControllerName = function($scope, $http, $log) {
    
    $scope.model['lesson_dialog'] = $scope.model.play.enroll;
    $scope.model.lesson_dialog.temptext = null;
    $scope.model.lesson_dialog.loading = false;
    

    
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

    /*
    Редактировать шаг учеником
     */
    $scope.edit_step = function(number) {
        var _step = $scope.get_step_by_number(number, {
            mode: 'edit'
        });
        $scope.model.lesson_dialog.temptext = _step.text;
    };

    /*
    Сохранение шага ответа ученика
     */
    $scope.save_step = function(number) {
        $scope.get_step_by_number(number, {
            text: $scope.model.lesson_dialog.temptext,
            mode: null
        });
        $scope.save();
    };

    /*
    Добавляем ответ учеником
     */
    $scope.add_answer_pupil = function() {
        $scope.model.lesson_dialog.temptext = null;
        $scope.model.lesson_dialog.data.steps.push({
            number: $scope.model.lesson_dialog.data.steps.length + 1,
            type: "pupil",
            text: "",
            mode: 'edit'
        });
    };

    /*
    Определяет есть ли возможность ответа на задание
    Появление кнопки и добавить ответ для ученика
     */
    $scope.get_answer_pupil = function() {
        if ($scope.model.lesson_dialog.data.active == true) {
            if ($scope.model.lesson_dialog.data.steps.length == 0 || $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].type == 'teacher') {
                return true;
            }
        }
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

    $scope.save = function() {
        $scope.model.lesson_dialog.loading = true;
        var _data = $scope.model.lesson_dialog.data;
        $http.put('/api/enroll_pupil/' + $scope.model.lesson_dialog.id + '/', JSON.stringify(_data))
            .then(function(result) {
                $scope.model.lesson_dialog.loading = false;
                $scope.model.lesson_dialog.data = result.data.data;
            }, function(error) {
                $scope.model.lesson_dialog.loading = false;
                $log.error(error);
            });
    };



    // сброс флага внимания со стороны ученика в случении закрытого урока
    if ($scope.model.lesson_dialog.hasOwnProperty('data') &&
        $scope.model.lesson_dialog.data.active == false) {
        if ($scope.model.lesson_dialog.required_attention_by_pupil == true) {
            $scope.save();
        }
    }


};