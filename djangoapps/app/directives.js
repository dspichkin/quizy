'use strict';

module.exports = angular.module('quizy.Directives', [])
    // Иерархия контроллеров
    .directive('tabs', require('./utils/tabs.js'))
    .directive('ripple', require('./utils/ripple.js'))
