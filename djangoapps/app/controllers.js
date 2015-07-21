'use strict';

module.exports = angular.module('quizy.Controllers', [])
    // Иерархия контроллеров
    .controller('SignupCtrl', require('./accounts/SignupController.js'))
    .controller('SignupConfirmCtrl', require('./accounts/SignupConfirmController.js'))
    .controller('ProfileCtrl', require('./accounts/ProfileController.js'))
    .controller('MainCtrl', require('./main/MainController.js'))
    .controller('CoursesTeacherCtrl', require('./main/CoursesTeacherController.js'))
    .controller('CourseTeacherCtrl', require('./main/CourseTeacherController.js'))
    .controller('LessonsTeacherCtrl', require('./main/LessonsTeacherController.js'))
    .controller('LessonsPupilCtrl', require('./main/LessonsPupilController.js'))
    .controller('PlayCtrl', require('./play/PlayController.js'))
    .controller('EditLessonCtrl', require('./editor/EditLessonController.js'))
