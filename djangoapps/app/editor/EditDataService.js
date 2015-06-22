'use strict';



module.exports = ['$http', function($http) {
    var url_pages = '/api/pages/';
    var url_lessons = '/api/lessons/';

    var _get_pages = function() {
        return $http.get(url_pages);
    };

    var _save_pages = function(data) {
        return $http.post(url_pages, data);
    };

    var _new_lesson = function() {
        return $http.post(url_lessons);
    };

    //var _remove_lesson = function(id) {
    //    return $http.delete(url_lessons + id + '/');
    //};

    var _get_lessons = function() {
        return $http.get(url_lessons);
    };

    var _get_lesson = function(id) {
        return $http.get(url_lessons + id + '/');
    };

    return {
        load_data: _get_pages,
        save_data: _save_pages,
        new_lesson: _new_lesson,
        get_lessons: _get_lessons,
        get_lesson: _get_lesson,
        //remove_lesson: _remove_lesson
    };
}];
