"use strict";

var _ = require('lodash-node/compat');

function BaseObject() {
    this.created_at;
    this.updated_at;

}

BaseObject.prototype.constructor = BaseObject;

_.assign(BaseObject.prototype, {
});


module.exports = BaseObject;