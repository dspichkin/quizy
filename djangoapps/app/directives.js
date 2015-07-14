'use strict';

module.exports = angular.module('quizy.Directives', [])
    // Иерархия контроллеров
    .directive('tabs', require('./utils/tabs.js'))
    .directive('ripple', require('./utils/ripple.js'))
    .directive('fab', require('./utils/fab.js'))
    .directive('lessonAction', require('./utils/lesson_action.js'))
    .directive('drag', require('./utils/drag.js'))

