'use strict';
/* globals
app:false

*/
app.ControllerName = function($scope, $http, $log, $sce, $timeout, $mdDialog) {
    if ($scope.model.play) {
        $scope.model.lesson_dialog = $scope.model.play.enroll;
    }
    
    if (!$scope.model.lesson_dialog) {
        $scope.model.lesson_dialog = {};
    }

    $scope.model.lesson_dialog.temptext = null;

    $scope.model.lesson_dialog.loading = false;
    // Переменные таймера
    $scope.stop_timer = false;
    $scope.disable_runtimer = false;

    detect_media_type();

    $scope.model.timer = $scope.model.lesson_dialog.lesson.timer;
    // количество слов
    $scope.model.number_words = 0;

    // Editor options.
    $scope.editorOptions = {
        language: 'ru',
        allowedContent: true,
        entities: false,
        height: '200px',
        resize_enabled: false,
        stylesSet: 'my_styles',
        extraPlugins: 'panelbutton,colorbutton'
    };
    // сброс флага внимания со стороны ученика
    // $scope.model.lesson_dialog.data.active == false
    if ($scope.model.lesson_dialog.hasOwnProperty('data')) {
        if ($scope.model.lesson_dialog.required_attention_by_pupil === true) {
            save();
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
                if (data.hasOwnProperty('number_words')) {
                    $scope.model.lesson_dialog.data.steps[i].number_words = data.number_words;
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
            mode: null,
            number_words: $scope.model.number_words
        });
        save();
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
        // если урок активен
        if ($scope.model.lesson_dialog.hasOwnProperty('data') && $scope.model.lesson_dialog.data.active === true) {
            // если нет ответов или последний ответ был от учителя
            if ($scope.model.lesson_dialog.data.steps.length === 0 ||
                ($scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].type == 'teacher' &&
                    $scope.model.lesson_dialog.data.steps[$scope.model.lesson_dialog.data.steps.length - 1].mode == 'finish')) {
                return true;
            }
        }
        return false;
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

    /*
    Завершение редактирование ответа
     */
    $scope.commit_step = function($event, number) {
        $mdDialog.show({
              targetEvent: $event,
              template:
                    '<md-dialog aria-label="List dialog">' +
                    '  <md-dialog-content style="padding:20px;">' +
                    '    <p><b translate>Send your text to teacher?</b>' +
                    '    <p translate>After confirming, you won’t be able to edit.</p>' +
                    '  </md-dialog-content>' +
                    '  <div class="md-actions">' +
                    '    <md-button ng-click="closeDialog()" class="md-primary">' +
                    '      <span translate>Cancel</span>' +
                    '    </md-button>' +
                    '    <button type="button" ng-click="submit($event)" class="btn-secondary" style="margin-left: 10px;">' +
                    '      <span translate>Send</span>' +
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
                        $scope.model.lesson_dialog.data.mode = 'wait_teacher';
                        save();
                        $mdDialog.hide();
                    };
                }
            });
    };

    function save(settings) {
        $scope.model.lesson_dialog.loading = true;
        var _data = $scope.model.lesson_dialog.data;
        if (settings) {
            for (var key in settings) {
                _data[key] = settings[key];
            }
        }
        $http.put('/api/enroll_pupil/' + $scope.model.lesson_dialog.id + '/', JSON.stringify(_data))
            .then(function(result) {
                $scope.model.lesson_dialog.loading = false;
                $scope.model.lesson_dialog.data = result.data.data;
            }, function(error) {
                $scope.model.lesson_dialog.loading = false;
                $log.error(error);
            });
    }


    $scope.runTimer = function() {
        var startTimer = function() {
            if ($scope.timer_success === true) {
                 $scope.timer_success = false;
            }
            if ($scope.model.timer <= 0 || $scope.stop_timer === true) {
                $scope.disable_runtimer = false;
                $scope.stop_timer = false;
                $scope.timer_success = true;
                return;
            } else {
                if ($scope.disable_runtimer === false) {
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
        if ($scope.timer_success === true) {
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
                    '  <md-dialog-content style="padding:20px;">' +
                    '    <md-input-container>' +
                    '       <label>Секунд</label>' +
                    '       <input type="text" ng-model="timer" ng-change="changeTimer()" required >' +
                    '       <div ng-if="message" style="color:red;">{{message}}</div>' +
                    '    </md-input-container>' +
                    '  </md-dialog-content>' +
                    '  <div class="md-actions">' +
                    '    <md-button ng-click="closeDialog()" class="md-primary">' +
                    '      <span translate>Отмена</span>' +
                    '    </md-button>' +
                    '    <md-button ng-click="submit($event)" class="btn-secondary">' +
                    '      <span translate>Подтвердить</span>' +
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

                    $scope.closeDialog = function($event) {
                        $mdDialog.hide();
                    };

                    $scope.changeTimer = function() {
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

                    $scope.submit = function($event) {
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
        if ($scope.model.lesson_dialog.lesson) {
            if (!$scope.model.lesson_dialog.lesson.media) {
                return;
            }
        } else {
            return;
        }

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

    $scope.change_text = function(text) {
        var _text;
        if (text) {
            _text = text;
        } else {
            _text = $scope.model.lesson_dialog.temptext;
        }

        if (_text) {
            $scope.model.number_words = $scope.get_number_words(_text);
        } else {
            $scope.model.number_words = 0;
        }
    };
    
    


    /**
     *
     * возвращает кол-во слов
     *
     */
    $scope.get_number_words = function(text) {
        if (text) {
            text = text.replace(/<(?:.|\n)*?>/gm, '');
            text = text.replace('&nbsp;', ' ');

            var _words = [];
            var temp = text.split(' ');

            for (var i = 0; i < temp.length; i++) {
                var t = temp[i].split('\n');

                // удаляем все пустые элементы в масивах t
                var _t1 = [];
                for (var j = 0; j < t.length; j++) {
                    t[j] = t[j].replace('\n', '');
                    if (t[j] !== '') {
                        _t1 = _t1.concat(t[j]);
                    }
                }

                if (_t1.length > 1) {
                    _words = _words.concat(_t1);
                } else {
                    temp[i] = temp[i].replace('\n', '');
                    if (temp[i] !== '') {
                        _words.push(temp[i]);
                    }
                }
            }

            if (_words && _words.length == 1) {
                if (_words[0] === "") {
                    return 0;
                } else {
                    return _words.length;
                }
            } else {
                return _words.length;
            }
        }
    };

    /*
    Начать урок выбраный через главную страницу
    */
    $scope.start_lesson = function(lesson_id) {
        $http.post('/api/start_lessons/' + lesson_id + '/')
            .then(function(data) {
                $scope.main.go_play(data.data.id);
            }, function(error) {
                $scope.model.lesson_dialog.loading = false;
                $log.error(error);
            });
    };

};