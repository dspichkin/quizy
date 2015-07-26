'use strict';

module.exports = angular.module('quizy.Controllers', [])
    // Иерархия контроллеров
    .controller('SignupCtrl', require('./accounts/SignupController.js'))
    .controller('SignupConfirmCtrl', require('./accounts/SignupConfirmController.js'))
    .controller('ProfileCtrl', require('./accounts/ProfileController.js'))
    .controller('MainCtrl', require('./main/MainController.js'))
    .controller('TeacherCoursesCtrl', require('./main/TeacherCoursesController.js'))
    .controller('TeacherCourseCtrl', require('./main/TeacherCourseController.js'))
    .controller('TeacherPupilCtrl', require('./main/TeacherPupilController.js'))
    .controller('PupilLessonsCtrl', require('./main/PupilLessonsController.js'))
    .controller('PlayCtrl', require('./play/PlayController.js'))
    .controller('EditLessonCtrl', require('./editor/EditLessonController.js'))
    //.controller('LessonsTeacherCtrl', require('./main/LessonsTeacherController.js'))
