"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');
var Lesson = require('./lesson');

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
        return $.ajax({
            url: "/api/answers/" + this.id + "/",
            data: this.serialize(),
            type: "PUT"
        });
    },
    make_result: function() {
        var last_question = false;
        var general_success = true;
        var step_reflexy = [];
        if (this.lesson.pages.length == this.answer_steps.length) {
            last_question = true;
        } else {
            general_success = false;
        }

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
                            if (_page_answer.item.answers[j].answer == true) {
                                num_answered_right_answer++;
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
                        // сравниваем по количеству ответов
                        if (_page_answer.item.answers.length != _page_answer.item.answers.length) {
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
                                        }
                                    }
                                }
                            }
                            // console.log('this.lesson.pages[i] ', this.lesson.pages[i])
                        }
                    }
                }

                step_reflexy.push({
                    page_id: this.lesson.pages[i].id,
                    success: _page_success
                });
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
