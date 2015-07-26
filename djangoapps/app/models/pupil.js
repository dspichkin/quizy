"use strict";

var _ = require('lodash-node/compat');
var BaseObject = require('./object');

function Pupil(data) {

    if (!(this instanceof Pupil)) return new Pupil(data);
    BaseObject.call(this);
    if (data == undefined) {
        console.log("Неверное создание объекта Pupil");
    }

    _.assign(this, data);
}

// Унаследуем BaseObject
Pupil.prototype = new BaseObject();
Pupil.prototype.constructor = Pupil;


_.assign(Pupil.prototype, {});


module.exports = Pupil;
