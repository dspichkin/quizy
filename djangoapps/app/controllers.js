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
    .controller('PlayBaseCtrl', require('./play/PlayBaseController.js'))
    .controller('PlayInsideCtrl', require('./play/PlayInsideController.js'))
    .controller('EditLessonCtrl', require('./editor/EditLessonController.js'))
    .controller('PupilStatisticCtrl', require('./main/PupilStatisticController.js'))
    .controller('TeacherStatisticCtrl', require('./main/TeacherStatisticController.js'))
