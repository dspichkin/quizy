'use strict';

app.ControllerName = function($scope, $http, $log, $mdDialog) {
    $scope.model['lesson_dialog'] = $scope.model.outside.enroll;
    $scope.model['lesson_dialog'].temptext = null;
    $scope.model.lesson_dialog.loading = false;

    // Editor options.
    $scope.editorOptions = {
        language: 'ru',
        allowedContent: true,
        entities: false,
        height: '200px',
        resize_enabled: false,
        extraPlugins: 'panelbutton,colorbutton'
    };


    $scope.back_to_lessons = function() {
        $scope.main.go_courses_page($scope.model.outside.course_id);

    };

    /*
    Определяет есть ли возможность написать ответ
     */
    $scope.get_answer_teacher = function() {
        if ($scope.model.lesson_dialog.data.steps.length > 0 &&
            $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].type == 'pupil' &&
            $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].mode == 'finish') {
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
            save();
        }
    };


    $scope.save_step = function(number) {
        $scope.get_step_by_number(number, {
            text: $scope.model.lesson_dialog.temptext,
            mode: null
        });

        save();
    };

    $scope.commit_step = function($event, number) {
        $mdDialog.show({
            targetEvent: $event,
            template:
                '<md-dialog aria-label="List dialog">' +
                '  <md-dialog-content>' +
                '    <p>После подтверждения редактирование будет невозможно</p>' +
                '  </md-dialog-content>' +
                '  <div class="md-actions">' +
                '    <md-button ng-click="closeDialog()" class="md-primary">' +
                '      Отмена' +
                '    </md-button>' +
                '    <button type="button" ng-click="submit($event)" class="btn-secondary" style="margin-left: 10px;">' +
                '      Подтвердить' +
                '    </button>' +
                '  </div>' +
                '</md-dialog>',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function TimerController($scope, $mdDialog) {
                scope.closeDialog = function($event) {
                    $mdDialog.hide();
                };
                scope.submit = function($event) {
                    $event.preventDefault();
                    $scope.get_step_by_number(number, {
                        mode: 'finish'
                    });
                    save();
                    $mdDialog.hide();
                };
            }
        });
    };


    function save() {
        var _data = $scope.model.lesson_dialog.data;
        $scope.model.lesson_dialog.loading = true;
        $http.put('/api/enroll_teacher/' + $scope.model.lesson_dialog.id + '/', JSON.stringify(_data))
            .then(function(result) {
                $scope.model.lesson_dialog.loading = false;
                $scope.model.lesson_dialog.data = result.data.data;
            }, function(error) {
                $scope.model.lesson_dialog.loading = false;
                $log.error(error);
            });
    };

    $scope.commit = function() {
        save();
    };

    $scope.get_number_words = function(text) {
        var _words = text.split(' ');
        if (_words && _words.length == 1) {
            if (_words[0] == "") {
                return 0;
            } else {
                return _words.length;
            }
        } else {
            return _words.length;
        }
    }

}