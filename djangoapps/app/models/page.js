"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');

function Page(data) {

    if (!(this instanceof Page)) return new Page(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта page");
    }

    if (data.type == 'pairs') {
        var _raw_variants = data.variants;
        var _new_variants = [];
        for (var i = 0, len = _raw_variants.length; i < len; i++) {
            if (_raw_variants[i].pair_type == "answer") {
                var _answer = _raw_variants[i];
                var _page;
                for (var j = 0, len = _raw_variants.length; j < len; j++) {
                    if (_raw_variants[j].id == _answer.pair) {
                        _page = _raw_variants[j];
                        _page.pair_object = _answer;
                        _new_variants.push(_page);
                    }
                }
            }
        }
        data.variants = _new_variants;
    }

    _.assign(this, data);
}

// Унаследуем GameObject
Page.prototype = new BaseObject();
Page.prototype.constructor = Page;


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
    serialize: function() {
        return JSON.stringify({
            id: this.id,
            created_at: this.created_at,
            updated_at: this.updated_at,
            type: this.type,
            text: this.text,
            number: this.number,
            is_correct: this.is_correct,
            code_errors: this.code_errors,
            variants: this.variants
        });
    }

});

module.exports = Page;