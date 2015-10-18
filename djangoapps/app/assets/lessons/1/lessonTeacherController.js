'use strict';

app.ControllerName = function($scope, $http, $log, $sce, $mdDialog) {
    $scope.model.lesson_dialog = $scope.model.outside.enroll;
    $scope.model.lesson_dialog.temptext = null;
    $scope.model.lesson_dialog.loading = false;

    // Editor options.
    $scope.editorOptions = {
        language: 'en',
        allowedContent: true,
        entities: false,
        height: '200px',
        resize_enabled: false,
        //stylesSet: 'my_styles',
        extraPlugins: 'panelbutton,colorbutton,redbutton'
        
    };


    detect_media_type();

    // сброс флага внимания со стороны ученика
    // $scope.model.lesson_dialog.data.active == false
    if ($scope.model.lesson_dialog.hasOwnProperty('data')) {
        if ($scope.model.lesson_dialog.required_attention_by_teacher === true) {
            save();
        }
    }



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
        $scope.model.lesson_dialog.temptext = null;
        var _text_pupil = "";
        if ($scope.model.lesson_dialog.data.steps.length > 0) {
            _text_pupil = $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].text;
        }
        $scope.model.lesson_dialog.temptext = _text_pupil;
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
                if (data.hasOwnProperty('estimate')) {
                    $scope.model.lesson_dialog.data.steps[i].estimate = data.estimate;
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
        if (index !== null) {
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
                '   <p>Ready to send the feedback to the student?</p>' +
                '   <p>After confirming, you won’t be able to edit your comments.</p>' +
                '  </md-dialog-content>' +
                '  <div class="md-actions">' +
                '    <md-button ng-click="closeDialog()" class="md-primary">' +
                '      Cancel' +
                '    </md-button>' +
                '    <button type="button" ng-click="submit($event)" class="btn-secondary" style="margin-left: 10px;">' +
                '      Confirm' +
                '    </button>' +
                '  </div>' +
                '</md-dialog>',
            disableParentScroll: true,
            clickOutsideToClose: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function TimerController($scope, $mdDialog) {
                $scope.closeDialog = function($event) {
                    $mdDialog.hide();
                };
                $scope.submit = function($event) {
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
    }

    $scope.commit = function() {
        save();
    };

    $scope.get_number_words = function(text) {
        var _words = text.split(' ');
        if (_words && _words.length == 1) {
            if (_words[0] === "") {
                return 0;
            } else {
                return _words.length;
            }
        } else {
            return _words.length;
        }
    };

    /*
    Поставить оценку
     */
    $scope.estimate = function($event, step_number) {
        $mdDialog.show({
            targetEvent: $event,
            templateUrl: '/assets/lessons/1/estimate.html',    
            disableParentScroll: true,
            scope: $scope,        // use parent scope in template
            preserveScope: true,
            controller: function TimerController($scope, $mdDialog) {
                var curent_step = '';
                for (var i = 0, len = $scope.model.lesson_dialog.data.steps.length; i < len; i++) {
                        if ($scope.model.lesson_dialog.data.steps[i].number == step_number) {
                            curent_step = $scope.model.lesson_dialog.data.steps[i];
                        }
                    }


                $scope.model.estimate = {
                    commit_disabled: true,
                    estimate_task: '',
                    estimate_task_varinats: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                    coherence_task: '',
                    coherence_task_varinats: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                    lexical_task: '',
                    lexical_task_varinats: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
                    grammatical_task: '',
                    grammatical_task_varinats: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
                };
                if (curent_step) {
                    if (curent_step.estimate && curent_step.estimate.estimate_task)
                        $scope.model.estimate.estimate_task = curent_step.estimate.estimate_task;
                    if (curent_step.estimate && curent_step.estimate.coherence_task)
                        $scope.model.estimate.coherence_task = curent_step.estimate.coherence_task;
                    if (curent_step.estimate && curent_step.estimate.lexical_task)
                        $scope.model.estimate.lexical_task = curent_step.estimate.lexical_task;
                    if (curent_step.estimate && curent_step.estimate.grammatical_task)
                        $scope.model.estimate.grammatical_task = curent_step.estimate.grammatical_task;
                }

                $scope.change = function() {
                    if (is_ready() === true) {
                        $scope.model.estimate.commit_disabled = false;
                    }
                };

                $scope.closeDialog = function($event) {
                    $mdDialog.hide();
                };

                $scope.submit = function($event) {
                    $event.preventDefault();
                    var _data = {
                        estimate_task: $scope.model.estimate.estimate_task,
                        coherence_task: $scope.model.estimate.coherence_task,
                        lexical_task: $scope.model.estimate.lexical_task,
                        grammatical_task: $scope.model.estimate.grammatical_task
                    };
                    for (var i = 0, len = $scope.model.lesson_dialog.data.steps.length; i < len; i++) {
                        if ($scope.model.lesson_dialog.data.steps[i].number == step_number) {
                            $scope.model.lesson_dialog.data.steps[i].estimate = _data;
                        }
                    }

                    $mdDialog.hide();
                    save();
                };

                function is_ready() {
                    var _is_ready = true;
                    if ($scope.model.estimate.estimate_task === "") {
                        _is_ready = false;
                    }
                    if ($scope.model.estimate.coherence_task === "") {
                        _is_ready = false;
                    }
                    if ($scope.model.estimate.lexical_task === "") {
                        _is_ready = false;
                    }
                    if ($scope.model.estimate.grammatical_task === "") {
                        _is_ready = false;
                    }
                    return _is_ready;
                }
            }
        });
    };


    // Опеределяем тип медиа
    function detect_media_type() {
        var _filename = $scope.model.lesson_dialog.lesson.media;
        if (_filename) {
            var _ext = _filename.substr(_filename.length - 3);
            if (_ext.toLowerCase() == 'mp4') {
                $scope.model.lesson_dialog.lesson.media_type = 'video';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.lesson_dialog.lesson.media),
                    type: "video/mp4"
                }];
            }
            if (_ext.toLowerCase() == 'webm') {
                $scope.model.lesson_dialog.lesson.media_type = 'video';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.lesson_dialog.lesson.media),
                    type: "video/webm"
                }];
            }
            if (_ext.toLowerCase() == 'mp3') {
                $scope.model.lesson_dialog.lesson.media_type = 'audio';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.lesson_dialog.lesson.media),
                    type: "audio/mp3"
                }];
            }
            if (_ext.toLowerCase() == 'jpg' || _ext.toLowerCase() == 'png' || _ext.toLowerCase() == 'gif') {
                $scope.model.lesson_dialog.lesson.media_type = 'image';
            }
        }
    }

};