'use strict';


var ArticlesCtrl = function($scope, $stateParams) {

	var _templates = [{
		slug: 'aboutielts.html',
		template: '/assets/partials/articles/articles/aboutielts.html'
	}, {
		slug: 'writing.html',
		template: '/assets/partials/articles/articles/writing.html'
	}, {
		slug: 'prepearing.html',
		template: '/assets/partials/articles/articles/prepearing.html'
	}];

	$scope.main.make_short_header();
    $scope.main.active_menu = 'articles';

	start();

	$scope.getTemplate = function() {
        return $scope.template;
    };

	function start() {
		var _slug = $stateParams.slug;
		var _find = false;
		if (_slug) {
			for (var i = 0; i < _templates.length; i++) {
				if (_slug === _templates[i].slug) {
					_find = true;
					$scope.template = _templates[i].template;
				}
			}

			if (_find === false) {
				$scope.template = '/assets/partials/articles/articles/list.html';
        		return;
			}
		} else {
			$scope.template = '/assets/partials/articles/articles/list.html';
        	return;
		}
	}
};


module.exports = ['$scope', '$stateParams', ArticlesCtrl];