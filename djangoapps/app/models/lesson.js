"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');
var Page = require('./page');

function Lesson(data) {

    if (!(this instanceof Lesson)) return new Lesson(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта lesson");
    }

    _.assign(this, data);
    this.pages = [];
    for (var i = 0, len = data.pages.length; i < len; i++) {
        this.pages.push(new Page(data.pages[i]));
    }
}

// Унаследуем BaseObject
Lesson.prototype = new BaseObject();
Lesson.prototype.constructor = Lesson;

var _code_errors = {
    200: "Не заполнено имя урока",
    201: "Не заполнено описание урока",
    202: "Нет ни одной страницы урока"
};


_.assign(Lesson.prototype, {
    create: function(lesson_id) {
        return $.ajax({
            url: "/api/lessons/",
            data: this.serialize(),
            type: "POST"
        });
    },
    delete: function() {
        return $.ajax({
            url: "/api/lessons/" + this.id + "/",
            type: "DELETE"
        });
    },
    save: function() {
        return $.ajax({
            url: "/api/lessons/" + this.id + "/",
            data: this.serialize(),
            dataType: "json",
            type: "PUT"
        });
    },
    new_page: function(variant) {
        return $.ajax({
            url: "/api/lessons/" + this.id + "/new_page/",
            data: variant,
            type: "POST"
        });
    },
    remove_page: function(variant_id) {
        return $.ajax({
            url: "/api/lessons/" + this.id + "/remove_page/" + variant_id + "/",
            type: "DELETE"
        });
    },
    serialize: function() {
        return JSON.stringify({
            id: this.id,
            is_active: this.is_active,
            is_correct: this.is_correct,
            created_at: this.created_at,
            updated_at: this.updated_at,
            name: this.name,
            description: this.description,
            number: this.number,
            pages: this.pages,
            code_errors: this.code_errors
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
    remove_lesson_picture: function() {
        return $.ajax({
            url: "/api/lessons/" + this.id + "/upload/",
            type: "DELETE"
        });
    },
    check: function() {
        if (!this.name || this.name == "") {
            this.add_error('200');
        } else {
            this.remove_error('200');
        }
        if (!this.description || this.description == "") {
            this.add_error('201');
        } else {
            this.remove_error('201');
        }

        if (this.pages.length == 0) {
             this.add_error('202');
        } else {
            this.remove_error('202');
        }

        var _has_error = false;
        for (var i = 0, len = this.pages.length; i < len; i++) {
            this.pages[i].check();
            if (this.pages[i].is_correct == false) {
                _has_error = true;
            }
        }
        if (_has_error == true) {
            this.is_correct = false;
        } else {
            this.is_correct = true;
        }

        if (_has_error == false) {
            if (Object.keys(this.code_errors).length > 0) {
                this.is_correct = false;
            } else {
                this.is_correct = true;
            }
        }
    }

});


module.exports = Lesson;