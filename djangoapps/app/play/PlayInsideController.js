'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');
var Attempt = require('../models/attempt');

var PlayCtrl = function($scope, $sce, $http, $stateParams, $log, $location, $compile) {

    //для хранения радиобокс ответа
    $scope.tempdata = {
        'radiobox_answer': null,
        'text_answer': null
    };
    
    //$scope.main.make_short_header();
    //$scope.main.active_menu = 'lessons';

    
    $scope.model['inside_play'] = {
        current_page_index: 0,
        next_question: false,
        result: null,
        success: null,
        lesson: null,
        attempt: null
    };

    start();




    function start() {
        $scope.model.inside_play.current_page_index = 0;
        if ($stateParams.enroll_id) {
            load_enroll($stateParams.enroll_id);
        } else if ($stateParams.lesson_id) {
            load_lesson($stateParams.lesson_id);
            
        } else {
            return;
        }
    };


    function load_enroll(enroll_id) {
        $http.get('/api/play/' + enroll_id + "/").then(function(data) {
            $scope.model.inside_play.attempt = new Attempt(data.data);
            var _p = $scope.model.inside_play.attempt.lesson.pages;
            if (_p.length > 0 && _p[$scope.model.inside_play.current_page_index].media) {
                $scope.detect_media_type();
            }
            $scope.answer_ready();
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });
    };

    function load_lesson(lesson_id) {
        $http.get('/api/demo/play/' + lesson_id + "/").then(function(data) {
            $scope.model.inside_play.attempt = new Attempt(data.data);
            var _p = $scope.model.inside_play.attempt.lesson.pages;
            if (_p.length > 0 && _p[$scope.model.inside_play.current_page_index].media) {
                $scope.detect_media_type();
            }
            $scope.answer_ready();
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });
    };


    function run_make_word_in_text() {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        if (_pages[$scope.model.inside_play.current_page_index].type == 'words_in_text') {
            /*
            Формируем модель для отображения select
            text - конечтный текст для отображения в шаблоне
            select - список селектов
            select = [
                {
                    selected - ответ выбранный пользователем
                    options - варианты выбора
                    options = [{
                        answer: true,
                        text: "xxx"
                    }]
                }
            ]
             */
            $scope.words_in_text = {
                text: null,
                select: [],
                input: []
            };
            var _variants = _pages[$scope.model.inside_play.current_page_index].variants;
            // проходим по все вариантам (сейчас всегда один)
            for (var i = 0, len = _variants.length; i < len; i++) {
                var _text = _variants[i].text;
                // Формируем все SELECT
                var _selects = _variants[i].right_answers_select;
                if (_selects) {
                    for (var j = 0, lenj = _selects.length; j < lenj; j++) {
                        var _words = _selects[j].words;
                        $scope.words_in_text.select[j] = {
                            options: _words
                        };
                        var _select_html = ' <select ng-model="words_in_text.select[' + j + '].selected"' +
                            ' ng-options="item.text for item in words_in_text.select[' + j + '].options" ' +
                            'ng-change="change_words_in_text()"></select>';

                        _selects[j].source = _selects[j].source.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
                        var re = new RegExp(_selects[j].source, "g");
                        _text = _text.replace(re, _select_html);
                    }
                }

                // Формируем все INPUT
                var _inputs = _variants[i].right_answers_input;
                if (_inputs) {
                    for (var j = 0, lenj = _inputs.length; j < lenj; j++) {
                        var _words = _inputs[j].words;
                        $scope.words_in_text.input[j] = {
                            options: _words
                        };
                        var _input_html = ' <input ng-model="words_in_text.input[' + j + '].inputed"' +
                            'ng-change="change_words_in_text()" />';

                        _inputs[j].source = _inputs[j].source.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
                        var re = new RegExp(_inputs[j].source, "g");
                        _text = _text.replace(re, _input_html);
                    }
                }

                $scope.words_in_text.text = _text;
            }
        }
    }

    /**
     * Запись тесктового ответа
     * @param  {[type]} _id [description]
     * @return {[type]}     [description]
     */
    $scope.answer_text = function(_id) {
        $scope.tempdata.text_answer = {
            text: $scope.tempdata.text_answer_temp,
            variant_id: _id
        };
        if ($scope.tempdata.text_answer.text) {
            $scope.model.inside_play.next_question = true;
        } else {
            $scope.model.inside_play.next_question = false;
        }
    };

    // обработчки изменнений в words_in_text
    $scope.change_words_in_text = function() {
        // проверяем если не отвеченные слова
        var _has_all_answers = true;
        // проходим по всем селектам и проверем есть ли selected
        for (var i = 0, len = $scope.words_in_text.select.length; i < len; i++) {
            if (!$scope.words_in_text.select[i].hasOwnProperty('selected')) {
                _has_all_answers = false;
                break;
            }
        }

        // проходим по всем инпутам и проверем есть ли inputed и оно не пустое
        if (_has_all_answers == true) {
            for (var i = 0, len = $scope.words_in_text.input.length; i < len; i++) {
                if (!$scope.words_in_text.input[i].hasOwnProperty('inputed')) {
                    _has_all_answers = false;
                    break;
                } else {
                    if ($scope.words_in_text.input[i].inputed == "") {
                        _has_all_answers = false;
                        break;
                    }
                }
            }
        }

        if ($scope.model.inside_play.next_question != _has_all_answers) {
            $scope.model.inside_play.next_question = _has_all_answers;
            // Записываем результат в текущую попытку для дальнейшего просчета
            var _pages = $scope.model.inside_play.attempt.lesson.pages;
            var _step = $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index];
            if (_step) {
                _step.answers = $scope.words_in_text;
            } else {
                _step = {
                    'type': 'words_in_text',
                    'page_id': _pages[$scope.model.inside_play.current_page_index].id,
                    'answers': $scope.words_in_text
                };
            }
            $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index] = _step;

            setTimeout(function() {
                $scope.$digest();
            });
        }
    };



    function has_answer() {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        if (_pages.hasOwnProperty($scope.model.inside_play.current_page_index)) {
            if (_pages[$scope.model.inside_play.current_page_index].type == 'checkbox') {
                var _variants = _pages[$scope.model.inside_play.current_page_index].variants;
                for (var i = 0, len = _variants.length; i < len; i++) {
                    if (_variants[i].answer == true) {
                        return true;
                    }
                }
            }
            if (_pages[$scope.model.inside_play.current_page_index].type == 'radiobox') {
                if ($scope.tempdata.radiobox_answer) {
                    return true;
                }
            }

            if (_pages[$scope.model.inside_play.current_page_index].type == 'pairs') {
                var _current_answers = $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index];
                // проверяем количество текущих ответов с ниобходим кол-вом ответов
                var _required_answers = _pages[$scope.model.inside_play.current_page_index].variants.length / 2;
                var _current_answers_number = 0;
                if (_current_answers) {
                    for (var i in _current_answers.answers) {
                        if (_current_answers.answers[i].answer) {
                            _current_answers_number++;
                        }
                    }

                    if (_current_answers_number == _required_answers) {
                        return true;
                    } else {
                        return false;
                    }
                }
            }

        }
        return false;

    };

    // Проверяем дан ли ответ и можно переходи к следующему вопросу
    $scope.answer_ready = function() {
        if ($scope.model.inside_play.current_page_index < $scope.model.inside_play.attempt.lesson.pages.length) {
            run_make_word_in_text();
        }

        if ($scope.model.inside_play.next_question != has_answer()) {
            $scope.model.inside_play.next_question = has_answer();
            setTimeout(function() {
                $scope.$digest();
            });
        }
    };



    /**
     * Делаем ответ для pairs
     * @param  {[type]} question_id [description]
     * @param  {[type]} answer_id   [description]
     * @return {[type]}             [description]
     */
    $scope.make_answer_for_pairs = function(question_id, answer_id) {
        // записывае ответ сделанный пользователем
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        if (_pages[$scope.model.inside_play.current_page_index].type == 'pairs') {
            var _variants = _pages[$scope.model.inside_play.current_page_index].variants;
            var _step = $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index];
            if (_step) {
                _step.answers[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            } else {
                _step = {
                    'type': 'pairs',
                    'page_id': _pages[$scope.model.inside_play.current_page_index].id,
                    'answers': {}
                };
                _step.answers[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            }

            $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index] = _step;
            $scope.answer_ready();
        }
    };


    // возвращает страницу по его id используеться в выдочи результатов
    $scope.get_page_by_id = function(page_id) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        for (var i = 0, len = _pages.length; i < len; i++) {
            if (_pages[i].id == page_id) {
                return _pages[i];
            }
        }
    };

    // возвращает true если найдена соотвествущая рефлексия
    $scope.get_reflexy = function(page_id, variant_id) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        for (var i = 0, len = _pages.length; i < len; i++) {
            if (_pages[i].id == page_id) {
                for (var j = 0, lenj = _pages[i].variants.length; j < lenj; j++) {
                    if (_pages[i].variants[j].id == variant_id) {
                        return true;
                    }
                }
            }
        }
    };

    // возвращает рефлексию ответа по его id используеться в выдочи результатов
    $scope.get_reflexy_by_id = function(page_id, variant_id) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        for (var i = 0, len = _pages.length; i < len; i++) {
            if (_pages[i].id == page_id) {
                for (var j = 0, lenj = _pages[i].variants.length; j < lenj; j++) {
                    if (_pages[i].variants[j].id == variant_id) {
                        return _pages[i].variants[j].reflexy;
                    }
                }
            }
        }
    };


    // возвращает вариант ответа по его id используеться в выдочи результатов
    $scope.get_variant_by_id = function(page_id, variant_id) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        for (var i = 0, len = _pages.length; i < len; i++) {
            if (_pages[i].id == page_id) {
                for (var j = 0, lenj = _pages[i].variants.length; j < lenj; j++) {
                    if (_pages[i].variants[j].id == variant_id) {
                        // console.log("! ", _pages[i].variants[j])
                        return _pages[i].variants[j].text;
                    }
                }
            }
        }
    };


    // возвращает статус варианта ответа по его id используеться в выдочи результатов
    $scope.id_correct_variant_by_id = function(page_id, variant_id) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        for (var i = 0, len = _pages.length; i < len; i++) {
            if (_pages[i].id == page_id) {
                for (var j = 0, lenj = _pages[i].variants.length; j < lenj; j++) {
                    if (_pages[i].variants[j].id == variant_id) {
                        return _pages[i].variants[j].right_answer;
                    }
                }
            }
        }
    };


    $scope.detect_media_type = function() {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        var _filename = _pages[$scope.model.inside_play.current_page_index].media;
        if (_filename) {
            var _ext = _filename.substr(_filename.length - 3);
            if (_ext == 'mp4') {
                $scope.model.inside_play.media_type = 'video';
                $scope.model.inside_play.media_sources = [{
                    src: $sce.trustAsResourceUrl(_pages[$scope.model.inside_play.current_page_index].media),
                    type: "video/mp4"
                }];
            }
            if (_ext == 'webm') {
                $scope.model.inside_play.media_type = 'video';
                $scope.model.inside_play.media_sources = [{
                    src: $sce.trustAsResourceUrl(_pages[$scope.model.inside_play.current_page_index].media),
                    type: "video/webm"
                }];
            }
            if (_ext == 'mp3') {
                $scope.model.inside_play.media_type = 'audio';
                $scope.model.inside_play.media_sources = [{
                    src: $sce.trustAsResourceUrl(_pages[$scope.model.inside_play.current_page_index].media),
                    type: "audio/mp3"
                }];
            }
            if (_ext == 'jpg' || _ext == 'png' || _ext == 'gif') {
                $scope.model.inside_play.media_type = 'image';
            }
        }
    };



    $scope.next_question = function($event) {
        var _pages = $scope.model.inside_play.attempt.lesson.pages;
        // записывае текущий ответ
        var _page_type = _pages[$scope.model.inside_play.current_page_index].type;
        console.log("111 ", _pages[$scope.model.inside_play.current_page_index].media)
        if (_pages[$scope.model.inside_play.current_page_index].media) {
            console.log("111 ", $scope.detect_media_type())
            $scope.detect_media_type();
        }

        if (_page_type == 'checkbox') {
            var _step = $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index];
            var _variants = _pages[$scope.model.inside_play.current_page_index].variants;
            var _answers = {
                'type': 'checkbox',
                'page_id': _pages[$scope.model.inside_play.current_page_index].id,
                'answers': []
            };

            for (var i = 0, len = _variants.length; i < len; i++) {
                if (_variants[i].hasOwnProperty('answer')) {
                    _answers.answers.push({
                        'variant_id': _variants[i].id,
                        'answer': _variants[i].answer
                    });
                } else {
                    _answers.answers.push({
                        'variant_id': _variants[i].answer,
                        'answer': false
                    });
                }
            }

            $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index] = _answers;
        }

        if (_page_type == 'radiobox') {
            var _answers = {
                'type': 'radiobox',
                'page_id': _pages[$scope.model.inside_play.current_page_index].id,
                'answers': [{
                    'variant_id': $scope.tempdata.radiobox_answer,
                    'answer': true
                }]
            };
            $scope.tempdata.radiobox_answer = null;
            $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index] = _answers;
        }

        if (_page_type == 'text') {
            var _answers = {
                'type': 'text',
                'page_id': _pages[$scope.model.inside_play.current_page_index].id,
                'answers': [{
                    'variant_id': $scope.tempdata.text_answer.variant_id,
                    'answer': $scope.tempdata.text_answer.text
                }]
            };
            $scope.tempdata.text_answer_temp = null;
            $scope.model.inside_play.attempt.answer_steps[$scope.model.inside_play.current_page_index] = _answers;
        }


        // сохраняем текущий ход
        $scope.model.inside_play.attempt.current_step = $scope.model.inside_play.current_page_index;
        $scope.model.inside_play.attempt.save();



        // переход к следующей страницы
        if ($scope.model.inside_play.next_question == true) {
            $scope.model.inside_play.current_page_index++;
            if ($scope.model.inside_play.current_page_index >= _pages.length) {
                $scope.model.inside_play.current_page_index = _pages.length;
            }
        }

        // Конец урока
        // Считаем результаты прохождения
        if ($scope.model.inside_play.current_page_index == _pages.length) {
            $scope.model.inside_play.attempt.make_result();
            $scope.model.inside_play.attempt.save();
            // считаем кол-во правильных и непрпвильных ответов
            var _steps = $scope.model.inside_play.attempt.result.steps;
            $scope.success = 0;
            $scope.number_steps = _steps.length;
            for (var i = 0, len = _steps.length; i < len; i++) {
                if (_steps[i].success == true) {
                    $scope.success += 1;
                }
            }
        }

        $scope.answer_ready();
        //$scope.get_answer_result();
    };


    $scope.repeat = function() {
        start();
    };


    $scope.back_to_start = function() {
        if ($stateParams.enroll_id) {
            if ($scope.model.inside_play.attempt.lesson.course.id) {
                $scope.main.go_courses_page($scope.model.inside_play.attempt.lesson.course.id);
            } else {
                $scope.main.go_courses_page();
            }
        }
    };


};


module.exports = ['$scope', '$sce', '$http', '$stateParams', '$log', '$location', '$compile', PlayCtrl];


