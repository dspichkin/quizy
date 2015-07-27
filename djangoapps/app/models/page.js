"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');

function Page(data) {

    if (!(this instanceof Page)) return new Page(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта page");
    }

    // Формируем для words_in_text исходные данные
    if (data.type == 'words_in_text') {
        var _parse_str = function(data, type) {
            /*
            Функция для парсинга списка ввиде  ["[[ccc, fff, 222]]", ...] или  ["((ccc, fff, 222))", ...]
            в спискок формата
                _selects = [{
                    words: [{
                        answer: true,
                        text: "xxx"
                    }, {
                        answer: true,
                        text: "yyy"
                    }],
                    source: "\(\(xxx, yyy,zzz\)\)"
                }]
            */
            var _selects = [];

            for (var j = 0, lenj = data.length; j < lenj; j++) {
                var t1 = data[j].substring(2, data[j].length - 2);
                var t2 = [];
                if (t1.length > 0) {
                    t2 = t1.split(',');
                    var _words = [];
                    // убираем пробелы
                    for (var x = 0, lenx = t2.length; x < lenx; x++) {
                        var _current_word = t2[x].trim();
                        // если текущее слово начинаеться с * помечаем только его как правильно
                        if (type == 'select') {
                            if (t2[x].trim()[0] == '*') {
                                _words.push({
                                    text: _current_word.substring(1, _current_word.length),
                                    answer: true

                                });
                            } else {
                                _words.push({
                                    text: _current_word,
                                    answer: false
                                });
                            }
                        } else {
                            _words.push({
                                text: _current_word,
                                answer: true

                            });
                        }
                    }
                    if (t2.length > 0) {
                        _selects.push({
                            source: data[j],
                            words: _words
                        });
                    }
                }
            }
            return _selects;
        };

        var _raw_variants = data.variants;
        // проходим по всем варианта сейчас только один
        for (var i = 0, len = _raw_variants.length; i < len; i++) {
            // подготавливаем данные
            var _text = _raw_variants[i].text;
            // ищем все селекты
            var _sel = _text.match(/\(\(.*?\)\)/g);
            // ищем все инпуты
            var _inp = _text.match(/\[\[.*?\]\]/g);

            if (_sel && _sel.length > 0) {
                _raw_variants[i].right_answers_select = _parse_str(_sel, 'select');
            }
            if (_inp && _inp.length > 0) {
                _raw_variants[i].right_answers_input = _parse_str(_inp);
            }
            // console.log('_raw_variants', _raw_variants[i])
        }
    }

    _.assign(this, data);
}

// Унаследуем GameObject
Page.prototype = new BaseObject();
Page.prototype.constructor = Page;

var _code_errors = {
    300: "На одной или несколько страниц не заполнено поле вопроса",
    301: "На одной или несколько страниц не заполнен один из вариантов ответов"
};

_.assign(Page.prototype, {
    create: function(lesson_id) {
        return $.ajax({
            url: "/api/lessons/" + lesson_id + "/new_page/",
            data: this.serialize(),
            type: "POST"
        });
    },
    remove: function() {
        return $.ajax({
            url: "/api/pages/" + this.id + "/",
            type: "DELETE"
        });
    },
    save: function() {
        return $.ajax({
            url: "/api/pages/" + this.id + "/",
            data: this.serialize(),
            dataType: "json",
            type: "PUT"
        });
    },
    new_variant: function(variant) {
        return $.ajax({
            url: "/api/pages/" + this.id + "/new_variant/",
            data: variant,
            type: "POST"
        });
    },
    remove_variant: function(variant_id) {
        return $.ajax({
            url: "/api/pages/" + this.id + "/remove_variant/" + variant_id + "/",
            type: "DELETE"
        });
    },
    remove_page_media: function() {
        return $.ajax({
            url: 'api/pages/' + this.id + '/upload/',
            type: "DELETE"
        });
    },
    serialize: function() {
        return JSON.stringify({
            id: this.id,
            type: this.type,
            text: this.text,
            number: this.number,
            is_correct: this.is_correct,
            code_errors: this.code_errors,
            variants: this.variants
        });
    },
    add_error: function(index) {
        if (this.code_errors) {
            this.code_errors[index] = _code_errors[index];
        }
    },
    remove_error: function(index) {
        if (this.code_errors) {
            if (this.code_errors.hasOwnProperty(index)) {
                delete this.code_errors[index];
            }
        }
    },
    check: function() {
        if (!this.text || this.text == "") {
            this.add_error('300');
        } else {
            this.remove_error('300');
        }
        var _is_correct_variants = true;
        for (var i = 0, len = this.variants.length; i < len; i++) {
            if (this.variants[i].text == "") {
                this.add_error('301');
                _is_correct_variants = false;
            }
        }
        if (_is_correct_variants == true) {
            this.remove_error('301');
        }

        if (this.code_errors) {
            if (Object.keys(this.code_errors).length > 0) {
                this.is_correct = false;
            } else {
                this.is_correct = true;
            }
        }
    }

});

module.exports = Page;