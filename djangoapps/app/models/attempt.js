"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');

function Attempt(data) {
    if (!(this instanceof Attempt)) return new Attempt(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта attempt");
    }

    _.assign(this, data);

    this.answer_steps = [];

}


// Унаследуем BaseObject
Attempt.prototype = new BaseObject();
Attempt.prototype.constructor = Attempt;


_.assign(Attempt.prototype, {});


module.exports = Attempt;
