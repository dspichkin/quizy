'use strict';

var Page = require('../models/page');
var Lesson = require('../models/lesson');
var Attempt = require('../models/attempt');

var PlayCtrl = function($scope, $sce, $http, $stateParams, $log, $location, $compile) {

    if (!$scope.user || !$scope.user.is_authenticated) {
        $scope.main.run(function() {
            if (!$scope.user || !$scope.user.is_authenticated) {
                $scope.main.reset_menu();
                $location.path('/');
                return;
            }
        });
    }
    //для хранения радиобокс ответа
    $scope.tempdata = {
        'radiobox_answer': null,
        'text_answer': null
    };

    $scope.main.make_short_header();
    $scope.main.active_menu = 'lessons';






    $scope.model['play'] = {
        current_page_index: 0,
        next_question: false,
        result: null,
        success: null,
        lesson: null,
        attempt: null
    };

    var load_enroll = function(enroll_id) {
        $http.get('/api/play/' + enroll_id + "/").then(function(data) {
            $scope.model.play.attempt = new Attempt(data.data);
            if ($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media) {
                $scope.detect_media_type();
            }
            make_word_in_text();
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });
    };

    var load_lesson = function(lesson_id) {
        $http.get('/api/demo/play/' + lesson_id + "/").then(function(data) {
            $scope.model.play.attempt = new Attempt(data.data);
            if ($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media) {
                $scope.detect_media_type();
            }
            make_word_in_text()
        }, function(error) {
            $log.error('Ошибка получения назначенных на меня уроков', error);
        });
    };



    var start = function() {
        $scope.model.play.current_page_index = 0;
        if ($stateParams.enroll_id) {
            load_enroll($stateParams.enroll_id);
        } else if ($stateParams.lesson_id) {
            load_lesson($stateParams.lesson_id);
        } else {
            return;
        }
    };

    var make_word_in_text = function() {
        if ($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].type == 'words_in_text') {
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
            var _variants = $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].variants;
            // проходим по все вариантам (сейчас всегда один)
            for (var i = 0, len = _variants.length; i < len; i++) {
                var _text = _variants[i].text;
                // Формируем все SELECT
                var _selects = _variants[i].right_answers_select;

                for (var j = 0, lenj = _selects.length; j < lenj; j++) {
                    var _words = _selects[j].words;
                    $scope.words_in_text.select[j] = {
                        options: _words
                    };
                    var _select_html = ' <select ng-model="words_in_text.select[' + j + '].selected"' +
                        ' ng-options="item.text for item in words_in_text.select[' + j + '].options" ' +
                        'ng-change="test()"></select>';

                    _selects[j].source = _selects[j].source.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
                    var re = new RegExp(_selects[j].source, "g");
                    _text = _text.replace(re, _select_html);
                }
                
                // Формируем все INPUT
                var _inputs = _variants[i].right_answers_input;

                for (var j = 0, lenj = _inputs.length; j < lenj; j++) {
                    var _words = _inputs[j].words;
                    $scope.words_in_text.input[j] = {
                        options: _words
                    };
                    var _input_html = ' <input ng-model="words_in_text.input[' + j + '].inputed"' +
                        'ng-change="test()" />';

                    _inputs[j].source = _inputs[j].source.replace(/([.?*+^$[\]\\(){}|-])/g, "\\$1");
                    var re = new RegExp(_inputs[j].source, "g");
                    _text = _text.replace(re, _input_html);
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
            $scope.model.play.next_question = true;
        } else {
            $scope.model.play.next_question = false;
        }
    };

    $scope.test = function() {
        console.log("#####")
        console.log("@@@@", $scope.words_in_text)
    }

    $scope.toTrustedHTML = function(html) {
        //return $sce.trustAsHtml( html );
        html = '<div>' + html + '</div>';
        var e = $compile(html)($scope);
        return $sce.trustAsHtml(html);
    }



    var has_answer = function() {
        var _pages = $scope.model.play.attempt.lesson.pages;
        if (_pages.hasOwnProperty($scope.model.play.current_page_index)) {
            if (_pages[$scope.model.play.current_page_index].type == 'checkbox') {
                var _variants = _pages[$scope.model.play.current_page_index].variants;
                for (var i = 0, len = _variants.length; i < len; i++) {
                    if (_variants[i].answer == true) {
                        return true;
                    }
                }
            }
            if (_pages[$scope.model.play.current_page_index].type == 'radiobox') {
                if ($scope.tempdata.radiobox_answer) {
                    return true;
                }
            }

            if (_pages[$scope.model.play.current_page_index].type == 'pairs') {
                var _current_answers = $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index];
                // проверяем количество текущих ответов с ниобходим кол-вом ответов
                var _required_answers = $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].variants.length / 2;
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

    $scope.answer_ready = function() {
        $scope.model.play.next_question = has_answer();
        setTimeout(function() {
            $scope.$apply();
        });
    };

    /**
     * Делаем ответ для pairs
     * @param  {[type]} question_id [description]
     * @param  {[type]} answer_id   [description]
     * @return {[type]}             [description]
     */
    $scope.make_answer_for_pairs = function(question_id, answer_id) {
        // записывае ответ сделанный пользователем
        var _pages = $scope.model.play.attempt.lesson.pages;
        if (_pages[$scope.model.play.current_page_index].type == 'pairs') {
            var _variants = _pages[$scope.model.play.current_page_index].variants;
            var _step = $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index];
            if (_step) {
                _step.answers[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            } else {
                _step = {
                    'type': 'pairs',
                    'page_id': _pages[$scope.model.play.current_page_index].id,
                    'answers': {}
                };
                _step.answers[question_id] = {
                    answer: answer_id,
                    question: question_id
                };
            }

            $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index] = _step;
            $scope.answer_ready();
        }
    };

    $scope.get_page_by_id = function(id) {
        for (var i = 0, len = $scope.model.play.attempt.lesson.pages.length; i < len; i++) {
            if ($scope.model.play.attempt.lesson.pages[i].id == id) {
                return $scope.model.play.attempt.lesson.pages[i];
            }
        }
    };

    $scope.detect_media_type = function() {
        var _filename = $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media;
        if (_filename) {
            var _ext = _filename.substr(_filename.length - 3);
            if (_ext == 'mp4') {
                $scope.model.play.media_type = 'video';
                $scope.model.play.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media),
                    type: "video/mp4"
                }];
            }
            if (_ext == 'webm') {
                $scope.model.play.media_type = 'video';
                $scope.model.play.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media),
                    type: "video/webm"
                }];
            }
            if (_ext == 'mp3') {
                $scope.model.play.media_type = 'audio';
                $scope.model.play.media_sources = [{
                    src: $sce.trustAsResourceUrl($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media),
                    type: "audio/mp3"
                }];
            }
            if (_ext == 'jpg' || _ext == 'png' || _ext == 'gif') {
                $scope.model.play.media_type = 'image';
            }
        }
    };

    $scope.next_question = function($event) {
        //console.log($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index])
        // записывае текущий ответ
        var _page_type = $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].type;

        if ($scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].media) {
            $scope.detect_media_type();
        }

        if (_page_type == 'checkbox') {
            var _step = $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index];
            var _variants = scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].variants;
            var _answers = {
                'type': 'checkbox',
                'page_id': $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].id,
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

            $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index] = _answers;
        }

        if (_page_type == 'radiobox') {
            var _answers = {
                'type': 'radiobox',
                'page_id': $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].id,
                'answers': [{
                    'variant_id': $scope.tempdata.radiobox_answer,
                    'answer': true
                }]
            };
            $scope.tempdata.radiobox_answer = null;
            $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index] = _answers;
        }

        if (_page_type == 'text') {
            var _answers = {
                'type': 'text',
                'page_id': $scope.model.play.attempt.lesson.pages[$scope.model.play.current_page_index].id,
                'answers': [{
                    'variant_id': $scope.tempdata.text_answer.variant_id,
                    'answer': $scope.tempdata.text_answer.text
                }]
            };
            $scope.tempdata.text_answer_temp = null;
            $scope.model.play.attempt.answer_steps[$scope.model.play.current_page_index] = _answers;
        }


        // сохраняем текущий ход
        $scope.model.play.attempt.current_step = $scope.model.play.current_page_index;
        $scope.model.play.attempt.save();



        // переход к следующей страницы
        if ($scope.model.play.next_question == true) {
            $scope.model.play.current_page_index++;
            if ($scope.model.play.current_page_index >= $scope.model.play.attempt.lesson.pages.length) {
                $scope.model.play.current_page_index = $scope.model.play.attempt.lesson.pages.length;
            }
        }

        if ($scope.model.play.current_page_index == $scope.model.play.attempt.lesson.pages.length) {
            $scope.result = $scope.model.play.attempt.make_result();
            $scope.model.play.attempt.save();
        }

        $scope.answer_ready();
        //$scope.get_answer_result();
    };

    $scope.repeat = function() {
        start();
    };

    $scope.back = function() {
        $scope.main.go_lessons_page();
        /*
        if ($stateParams.enroll_id) {
            $scope.main.go_lessons_page();
        }

        if ($stateParams.lesson_id) {
           $scope.main.go_editor_lesson($stateParams.lesson_id);
        }
        */
    };

    // =========================================

    start();
};


module.exports = ['$scope', '$sce', '$http', '$stateParams', '$log', '$location', '$compile', PlayCtrl];


