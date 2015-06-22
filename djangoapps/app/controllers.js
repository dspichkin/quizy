'use strict';

module.exports = angular.module('quizy.Controllers', [])
    // Иерархия контроллеров
    .controller('LoginCtrl', require('./accounts/LoginController.js'))
    .controller('SignupCtrl', require('./accounts/SignupController.js'))
    .controller('SignupConfirmCtrl', require('./accounts/SignupConfirmController.js'))
    .controller('ProfileCtrl', require('./accounts/ProfileController.js'))
    .controller('MainCtrl', require('./main/MainController.js'))
    .controller('LessonsCtrl', require('./main/LessonsController.js'))
    .controller('PlayCtrl', require('./play/PlayController.js'))
    .controller('EditCtrl', require('./editor/EditController.js'))
    .controller('ModalInstanceLessonEnrollCtrl', require('./main/ModalLessonEnrollController.js'))