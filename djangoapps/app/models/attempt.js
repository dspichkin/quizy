"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');
var Lesson = require('./lesson');
/*
так же сипользуеться для записи ответов
должна содержать
this.answer_step = [
    {
        answers: {},
        page_id: x
        type: 'xxxx'
    }
    ...]

 */
function Attempt(data) {
    this.current_step = 0;
    this.answer_steps = [];

    if (!(this instanceof Attempt)) return new Attempt(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта attempt");
    }

    _.assign(this, data);

    if (this.hasOwnProperty('lesson')) {
        this.lesson = new Lesson(this.lesson);
        this.lesson.shuffle_pairs();
    }
    if (!this.id) {
        this.id = 0;
    }

}


// Унаследуем BaseObject
Attempt.prototype = new BaseObject();
Attempt.prototype.constructor = Attempt;


_.assign(Attempt.prototype, {
    serialize: function() {
        var data = {
            csrfmiddlewaretoken: this.csrfmiddlewaretoken,
            id: this.id,
            current_step: this.current_step,
            answer_steps: this.answer_steps
        };

        if (this.result) {
            data['result'] = this.result;
            data['success'] = this.result.success;
        }
        return JSON.stringify(data);
    },
    get_answer_by_page_id: function(id) {
        for (var i = 0, len = this.answer_steps.length; i < len; i++) {
            if (id == this.answer_steps[i].page_id) {
                return this.answer_steps[i];
            }
        }
    },
    save: function() {
        var self = this;
        return $.ajax({
            url: "/api/answers/" + this.id + "/",
            dataType: "json",
            beforeSend: function(xhr, settings) {
                if (self.csrfmiddlewaretoken) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", self.csrfmiddlewaretoken);
                    }
                }
            },
            data: this.serialize(),
            type: "PUT"
        });
    },
    /**
     * Считаем результат прохождения попытки
     * @return {[type]} [description]
     */
    make_result: function() {

        var last_question = false;
        var general_success = true;
        // для записи результатов шагов
        var step_reflexy = [];
        // количество не верных пар используеться в рефлексии
        var number_of_incorrect_pairs = null;

        if (this.lesson.pages.length == this.answer_steps.length) {
            last_question = true;
        } else {
            general_success = false;
        }

        // для хранения выбранных элементов
        var choiced_elements = [];

        if (last_question === true) {
            // проверяем кол-во страниц с кол-вом ответов
            if (this.lesson.pages.length != this.answer_steps.length) {
                general_success = false;
            }

            for (var i = 0, len = this.lesson.pages.length; i < len; i++) {
                var _page_answer;
                // получаем ответ
                var _ap = this.get_answer_by_page_id(this.lesson.pages[i].id);
                if (_ap) {
                    if (this.lesson.pages[i].id === _ap.page_id) {
                        _page_answer = {
                            item: this.answer_steps[i],
                            get_by_id: function(id) {
                                for (var x = 0, lenx = this.item.answers.length; x < lenx; x++) {
                                    if (this.item.answers[x].variant_id == id) {
                                        return this.item.answers[x];
                                    }
                                }
                            }
                        };
                    }
                }
                var _page_success = false;
                // сравнивает ответ проверяем все ли правильыне ответы есть в данных ответов
                if (_page_answer) {
                    _page_success = true;
                    if (this.lesson.pages[i].type == 'checkbox') {

                        // получем кол-во правильных ответов
                        var num_right_answer = 0;
                        for (var j = 0, lenj = this.lesson.pages[i].variants.length; j < lenj; j++) {
                            if (this.lesson.pages[i].variants[j].right_answer == true) {
                                num_right_answer++;
                            }
                        }
                        // получем кол-во правильных ответов из данных ответов
                        var num_answered_right_answer = 0;
                        for (var j = 0, lenj = _page_answer.item.answers.length; j < lenj; j++) {
                            // считаем количество данных ответов
                            if (_page_answer.item.answers[j].answer == true) {
                                num_answered_right_answer++;
                                // запишем все выбранные ответы
                                choiced_elements.push({
                                    variant_id: _page_answer.item.answers[j].variant_id
                                });
                            }
                        }
                        // сравниваем кол-во правильных ответов с данным кол-вом ответов
                        if (num_right_answer != num_answered_right_answer) {
                            _page_success = false;
                        }
                        if (_page_success) {
                            for (var j = 0, lenj = this.lesson.pages[i].variants.length; j < lenj; j++) {
                                if (this.lesson.pages[i].variants[j].right_answer == true) {
                                    if (!_page_answer.get_by_id(this.lesson.pages[i].variants[j].id)) {
                                        _page_success = false;
                                    } else {
                                        if (_page_answer.get_by_id(this.lesson.pages[i].variants[j].id).answer != true) {
                                             _page_success = false;
                                        }
                                    }
                                }
                            }
                        }
                    }

                    if (this.lesson.pages[i].type == 'radiobox') {
                        // запишем все выбранные ответы
                        for (var j = 0, lenj = _page_answer.item.answers.length; j < lenj; j++) {
                            choiced_elements.push({
                                variant_id: _page_answer.item.answers[j].variant_id
                            });
                        }
                        // проходим по всем варианта
                        for (var j = 0, lenj = this.lesson.pages[i].variants.length; j < lenj; j++) {
                            // получаем правильный ответ
                            if (this.lesson.pages[i].variants[j].right_answer == true) {
                                var _right_answer_id = this.lesson.pages[i].variants[j].id;
                                var _answer = _page_answer.get_by_id(_right_answer_id);
                                if (_answer) {
                                    if (_answer.answer != true) {
                                        _page_success = false;
                                    }
                                } else {
                                    _page_success = false;
                                }
                            }
                        }
                    }

                    if (this.lesson.pages[i].type == 'text') {
                        // проходим по всем варианта
                        for (var j = 0, lenj = this.lesson.pages[i].variants.length; j < lenj; j++) {
                            var _current_id = this.lesson.pages[i].variants[j].id;
                            var _answer = _page_answer.get_by_id(_current_id);
                            if (_answer) {
                                if (_answer.answer != this.lesson.pages[i].variants[j].text) {
                                    _page_success = false;
                                }
                            } else {
                                _page_success = false;
                            }
                        }
                    }

                    if (this.lesson.pages[i].type == 'pairs') {
                        var result = true;
                        // кол-во ответов
                        var _number_of_answers = 0;
                        for (var k in _page_answer.item.answers) if (_page_answer.item.answers.hasOwnProperty(k)) _number_of_answers++;
                        // сравниваем по количеству ответов
                        if (this.lesson.pages[i].variants.length / 2 != _number_of_answers) {
                            _page_success = false;
                        }
                        for (var j = 0, lenj = this.lesson.pages[i].variants.length; j < lenj; j++) {
                            // проходим по всем answer и сравниваем pair
                            if (this.lesson.pages[i].variants[j].pair_type == 'answer') {
                                // берем текущий id и pair
                                var _answer_id = this.lesson.pages[i].variants[j].id;
                                var _pair_id = this.lesson.pages[i].variants[j].pair;
                                // ищем в данных ответах
                                for (var x in _page_answer.item.answers) {
                                    if (_page_answer.item.answers[x].answer == _answer_id) {
                                        if (_page_answer.item.answers[x].question != _pair_id) {
                                            _page_success = false;
                                            number_of_incorrect_pairs += 1;
                                        }
                                    }
                                }
                            }
                        }
                    }

                    if (this.lesson.pages[i].type == 'words_in_text') {
                        var _answers = _page_answer.item.answers;
                        // Проверяем все селекты
                        for (var x = 0, lenx = _answers.select.length; x < lenx; x++) {
                            if (_answers.select[x].hasOwnProperty('selected')) {
                                if (_answers.select[x].selected.answer != true) {
                                    _page_success = false;
                                }
                            } else {
                                 _page_success = false;
                            }
                        }
                        // Проверяем все интпуты
                        for (var x = 0, lenx = _answers.input.length; x < lenx; x++) {
                            if (_answers.input[x].hasOwnProperty('inputed')) {
                                var _inputed_word_correct = false;
                                for (var y = 0, leny = _answers.input[x].options.length; y < leny; y++) {
                                    var _inpute_word = _answers.input[x].inputed.trim();
                                    var _correct_word = _answers.input[x].options[y].text.trim();
                                    if (_inpute_word == _correct_word) {
                                        _inputed_word_correct = true;
                                    }
                                }
                                if (_inputed_word_correct == false) {
                                    _page_success = false;
                                }
                            } else {
                                _page_success = false;
                            }
                        }
                    }
                }
                //записываем результат прохождения шага
                var _result = {
                    page_id: this.lesson.pages[i].id,
                    success: _page_success,
                    type: this.lesson.pages[i].type,
                    choiced_elements: choiced_elements
                };

                // прописываем кол-во пар для рефлексии
                if (this.lesson.pages[i].type == 'pairs') {
                    _result['number_of_pairs'] = this.lesson.pages[i].variants.length / 2;
                    if (number_of_incorrect_pairs) {
                        _result['number_of_correct_pairs'] = _result['number_of_pairs'] - number_of_incorrect_pairs;
                    } else {
                        _result['number_of_correct_pairs'] = _result['number_of_pairs'];
                    }
                }
                step_reflexy.push(_result);
            }
        }

        // проверяем general_success
        for (var i = 0, len = step_reflexy.length; i < len; i++) {
            if (step_reflexy[i].success != true) {
                general_success = false;
            }
        }

        this.result = {
            success: general_success,
            steps: step_reflexy
        };
    }
});


module.exports = Attempt;
