'use strict';

app.ControllerName = function($scope, $http, $log, $sce, $timeout, $mdDialog) {

    $scope.model['lesson_dialog'] = $scope.model.play.enroll;
    $scope.model.lesson_dialog.temptext = null;
    $scope.model.lesson_dialog.loading = false;
    // Переменные таймера
    $scope.stop_timer = false;
    $scope.disable_runtimer = false;

    detect_media_type();

    $scope.model.timer = $scope.model.lesson_dialog.lesson.timer;
    // количество слов
    $scope.model.number_words = 0;


    // сброс флага внимания со стороны ученика в случении закрытого урока
    if ($scope.model.lesson_dialog.hasOwnProperty('data') &&
        $scope.model.lesson_dialog.data.active == false) {
        if ($scope.model.lesson_dialog.required_attention_by_pupil == true) {
            $scope.save();
        }
    }


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
        $scope.change_text(_step.text);
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
        $scope.model.number_words = 0;
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


    $scope.runTimer = function() {
        var startTimer = function() {
            if ($scope.timer_success == true) {
                 $scope.timer_success = false;
            }
            if ($scope.model.timer <= 0 || $scope.stop_timer == true) {
                $scope.disable_runtimer = false;
                $scope.stop_timer = false;
                $scope.timer_success = true;
                return;
            } else {
                if ($scope.disable_runtimer == false) {
                    $scope.disable_runtimer = true;
                }
                $scope.model.timer -= 1;
                $timeout(startTimer, 1000);
            }
        };
        startTimer();
    };
    $scope.stopTimer = function() {
        $scope.stop_timer = true;
    };
    $scope.resetTimer = function() {
        $scope.stop_timer = true;
        if ($scope.timer_success == true) {
             $scope.timer_success = false;
        }
        if ($scope.model.lesson_dialog.lesson.timer) {
            $scope.model.timer = $scope.model.lesson_dialog.lesson.timer;
        } else {
            $scope.model.timer = 0;
        }
    };
    $scope.inputTimer = function($event) {
        if ($event) {
            $event.preventDefault();
        }
        $mdDialog.show({
              targetEvent: $event,
              template:
                    '<md-dialog aria-label="List dialog">' +
                    '  <md-dialog-content>' +
                    '    <md-input-container>' +
                    '       <label>Секунд</label>' +
                    '       <input type="text" ng-model="timer" ng-change="changeTimer()" required >' +
                    '       <div ng-if="message" style="color:red;">{{message}}</div>' +
                    '    </md-input-container>' +
                    '  </md-dialog-content>' +
                    '  <div class="md-actions">' +
                    '    <md-button ng-click="closeDialog()" class="md-primary">' +
                    '      Отмена' +
                    '    </md-button>' +
                    '    <md-button ng-click="submit($event)" class="btn-secondary">' +
                    '      Подтвердить' +
                    '    </md-button>' +
                    '  </div>' +
                    '</md-dialog>',
              disableParentScroll: true,
              clickOutsideToClose: true,
                scope: $scope,        // use parent scope in template
                preserveScope: true,
                controller: function TimerController($scope, $mdDialog) {
                    $scope.old_timer = 0;
                    $scope.message = null;
                    $scope.timer = $scope.model.timer;

                    scope.closeDialog = function($event) {
                        $mdDialog.hide();
                    };

                    scope.changeTimer = function() {
                        if (!$scope.timer) {
                            $scope.timer = 0;
                        }
                        var e = parseInt($scope.timer, 10);
                        if (isNaN(e)) {
                            $scope.timer = $scope.old_timer;
                        }
                        $scope.timer = Math.floor(e);

                        if ($scope.timer && String($scope.timer).length >= 6) {
                            $scope.timer = $scope.old_timer;
                        } else {
                            $scope.old_timer = $scope.timer;
                        }
                    };

                    scope.submit = function($event) {
                        $event.preventDefault();
                        if (!$scope.timer) {
                            $scope.timer = 0;
                            $scope.message = "Требуется ввести число";
                            return;
                        }

                        $scope.model.timer = $scope.timer;
                        $mdDialog.hide();
                    };
                }
            });
    };


    // Опеределяем тип медиа
    function detect_media_type() {
        var _filename = $scope.model.lesson_dialog.lesson.media;
        if (_filename) {
            var _ext = _filename.substr(_filename.length - 3);
            if (_ext == 'mp4') {
                $scope.model.lesson_dialog.lesson.media_type = 'video';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.lesson_dialog.lesson.media),
                    type: "video/mp4"
                }];
            }
            if (_ext == 'webm') {
                $scope.model.lesson_dialog.lesson.media_type = 'video';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.lesson_dialog.lesson.media),
                    type: "video/webm"
                }];
            }
            if (_ext == 'mp3') {
                $scope.model.lesson_dialog.lesson.media_type = 'audio';
                $scope.model.lesson_dialog.lesson.media_sources = [{
                    src: $sce.trustAsResourceUrl(scope.model.lesson_dialog.lesson.media),
                    type: "audio/mp3"
                }];
            }
            if (_ext == 'jpg' || _ext == 'png' || _ext == 'gif') {
                $scope.model.lesson_dialog.lesson.media_type = 'image';
            }
        }
    };

    $scope.change_text = function(text) {
        if (text) {
            $scope.model.number_words = $scope.get_number_words(text);
        } else {
            $scope.model.number_words = $scope.get_number_words($scope.model.lesson_dialog.temptext);
        }
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
    };



};