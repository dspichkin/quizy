'use strict';

app.ControllerName = function($scope) {
    $scope.model = {
        steps: null
    };

    $scope.model.steps = [
        {
            number: 1,
            type: "pupil",
            text: "Текст набранный учеником  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ipsum metus, mollis et mi vel, scelerisque cursus mi. Donec non dignissim est. Phasellus ultrices sed lorem quis imperdiet. Nullam quis nunc vehicula, feugiat eros et, sagittis eros. Morbi cursus risus sed sapien pharetra sollicitudin. Sed tortor orci, ultrices eget lacus eu, egestas commodo erat. Maecenas lorem libero, sagittis ac iaculis a, malesuada vel nisi. Fusce id quam nisl. Etiam nec elit vehicula, malesuada enim ac, dictum nisi. Duis tincidunt ex vel orci varius pharetra. Praesent pharetra augue nec massa fermentum semper."
        },
        {
            number: 2,
            type: "teacher",
            text: "Текст набранный преподователем Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ipsum metus, mollis et mi vel, scelerisque cursus mi. Donec non dignissim est. Phasellus ultrices sed lorem quis imperdiet. Nullam quis nunc vehicula, feugiat eros et, sagittis eros. Morbi cursus risus sed sapien pharetra sollicitudin. Sed tortor orci, ultrices eget lacus eu, egestas commodo erat. Maecenas lorem libero, sagittis ac iaculis a, malesuada vel nisi. Fusce id quam nisl. Etiam nec elit vehicula, malesuada enim ac, dictum nisi. Duis tincidunt ex vel orci varius pharetra. Praesent pharetra augue nec massa fermentum semper."
        }//,
        //{
        //    number: 3,
        //    type: "pupil",
        //    text: "Текст набранный учеником  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ipsum metus, mollis et mi vel, scelerisque cursus mi. Donec non dignissim est. Phasellus ultrices sed lorem quis imperdiet. Nullam quis nunc vehicula, feugiat eros et, sagittis eros. Morbi cursus risus sed sapien pharetra sollicitudin. Sed tortor orci, ultrices eget lacus eu, egestas commodo erat. Maecenas lorem libero, sagittis ac iaculis a, malesuada vel nisi. Fusce id quam nisl. Etiam nec elit vehicula, malesuada enim ac, dictum nisi. Duis tincidunt ex vel orci varius pharetra. Praesent pharetra augue nec massa fermentum semper."
        //},
    ]

    $scope.get_step_by_number = function(number, data) {
        for (var i = 0, len = $scope.model.steps.length; i < len; i++) {
            if ($scope.model.steps[i].number == number) {
                if (data.hasOwnProperty('text')) {
                    $scope.model.steps[i].text = data.text;
                }
                if (data.hasOwnProperty('mode')) {
                    $scope.model.steps[i].mode = data.mode;
                }
                return $scope.model.steps[i];
            }
        }
    };

    /*
    Редактировать шаг учеником
     */
    $scope.edit_step = function(number) {
        var step = $scope.get_step_by_number(number, {
            mode: 'edit'
        });
        $scope.model.temptext = step.text;
    };

    $scope.save_step = function(number) {
        $scope.get_step_by_number(number, {
            text: $scope.model.temptext,
            mode: null
        });
    };

    $scope.add_answer_pupil = function() {
        $scope.model.steps.push({
            number: $scope.model.steps.length + 1,
            type: "pupil",
            text: "",
            mode: 'edit'
        });
    };

    /*
    Появление кнопки и добавить ответ для ученика
     */
    $scope.get_answer_pupil = function() {
        if ($scope.model.steps.length == 0 || $scope.model.steps[$scope.model.steps.length - 1].type == 'teacher') {
            return true;
        }
    }
}