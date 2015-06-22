'use strict';

module.exports = angular.module('quizy.filters', [])
  .filter('htmlToPlaintext', function() {
    return function(text) {
      return String(text).replace(/<[^>]+>/gm, '');
    };
  }
);