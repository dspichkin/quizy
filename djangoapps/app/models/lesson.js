"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');

function Lesson(data) {

    if (!(this instanceof Lesson)) return new Lesson(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта lesson");
    }


    _.assign(this, data);
}

// Унаследуем BaseObject
Lesson.prototype = new BaseObject();
Lesson.prototype.constructor = Lesson;


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
            created_at: this.created_at,
            updated_at: this.updated_at,
            name: this.name,
            description: this.description,
            number: this.number,
            pages: this.pages
        });
    }

});

module.exports = Lesson;