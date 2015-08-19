'use script';


angular.module("demo", ["ngSanitize", "dialog"])
    .controller("ctrl",["$scope",function($scope) {
        $scope.examUrl = {
            "settings": {
            },
            "reflexy": [],
            "base": {
            },
            "first_step": "1",
            "steps": [
                {
                    "id": "1",
                    "data" : {
                        "text": "Фраза 1",
                        "audiofile": "media/audio/1.mp3",
                    },
                    "variants": [
                        {
                            "data": {
                                "text": "Вариант 1",
                                "audiofile": "media/audio/1.1.mp3",
                            },
                            "id": "1.1",
                            "reflexy": {
                                "next_step": "2"
                            }
                        },
                        {
                            "data": {
                                "text": "Вариант 2",
                                "audiofile": "media/audio/1.2.mp3",
                            },
                            "id": "1.2",
                            "reflexy": {
                                "next_step": "2"
                            }
                        }
                    ]
                },
                {
                    "id": "2",
                    "type": "input",
                    "data" : {
                        "text": "Фраза 2",
                        "audiofile": "media/audio/2.mp3",
                    },
                    "variants": [
                        {
                            "data": {
                                "text": "Phrase 1",
                                "audiofile": "media/audio/2.1.mp3",
                            },
                            "id": "2.1",
                            "reflexy": {
                                "next_step": "3"
                            }
                        }
                    ]
                },
                {
                    "id": "3",
                    "next_reflexy": "1",
                    "data" : {
                        "text": "Фраза 3",
                        "audiofile": "media/audio/3.mp3",
                    },
                    "variants": [
                        {
                            "data": {
                                "text": "Фраза 3 Вариант 1",
                                "audiofile": "media/audio/3.1.mp3",
                            },
                            "id": "3.1",
                            "reflexy": {
                            }
                        }
                    ]
                }
            ],
            "reflexy": [
                {
                    "data": {
                        "text": "Молодец !!!"
                    }, 
                    "id": "1", 
                    "success": true
                }, 
                {
                    "data": {
                        "text": "Плохо !!!"
                    }, 
                    "id": "2", 
                    "success": false
                }
            ]
        };

    }]);
