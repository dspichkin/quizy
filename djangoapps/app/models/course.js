"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');
var Lesson = require('./lesson');

function Course(data) {

    if (!(this instanceof Course)) return new Course(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта Course");
    }

    _.assign(this, data);
    this.lessons = [];
    for (var i = 0, len = data.lessons.length; i < len; i++) {
        this.lessons.push(new Lesson(data.lessons[i]));
    }
}

// Унаследуем BaseObject
Lesson.prototype = new BaseObject();
Lesson.prototype.constructor = Course;

var _code_errors = {
    200: "Не заполнено имя курса",
    201: "Не заполнено описание курса"
};


_.assign(Lesson.prototype, {
    create: function(lesson_id) {
        return $.ajax({
            url: "/api/courses/",
            data: this.serialize(),
            type: "POST"
        });
    },
    delete: function() {
        return $.ajax({
            url: "/api/courses/" + this.id + "/",
            type: "DELETE"
        });
    },
    save: function() {
        return $.ajax({
            url: "/api/courses/" + this.id + "/",
            data: this.serialize(),
            dataType: "json",
            type: "PUT"
        });
    },
    new_page: function(variant) {
        return $.ajax({
            url: "/api/courses/" + this.id + "/new_page/",
            data: variant,
            type: "POST"
        });
    },
    remove_lesson: function(lesson_id) {
        return $.ajax({
            url: "/api/courses/" + this.id + "/remove_lesson/" + lesson_id + "/",
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
            lessons: this.lessons,
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
    remove_course_picture: function() {
        return $.ajax({
            url: "/api/course/" + this.id + "/upload/",
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

        if (this.lessons.length == 0) {
             this.add_error('202');
        } else {
            this.remove_error('202');
        }

        var _has_error = false;
        for (var i = 0, len = this.lessons.length; i < len; i++) {
            this.lessons[i].check();
            if (this.lessons[i].is_correct == false) {
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


module.exports = Course;