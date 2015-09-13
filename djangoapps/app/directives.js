'use strict';

module.exports = angular.module('quizy.Directives', [])
    // Иерархия контроллеров
    .directive('tabs', require('./utils/tabs.js'))
    .directive('ripple', require('./utils/ripple.js'))
    .directive('fab', require('./utils/fab.js'))
    .directive('lessonAction', require('./utils/lesson_action.js'))
    .directive('courseAction', require('./utils/course_action.js'))
    .directive('drag', require('./utils/drag.js'))
    .directive('compile', require('./utils/compile.js'))
    .directive('dynamicCtrl', require('./utils/dynamic_ctrl.js'))


