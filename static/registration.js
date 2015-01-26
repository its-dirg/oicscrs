var app = angular.module('main', ['ngSanitize']);

app.factory('static_client_factory', function ($http) {
    return {
        generate_client_credentials: function (redirect_uris) {
            return $http.post("/generate_client_credentials", {"redirect_uris": redirect_uris});
        }
    };
});

app.controller('IndexCtrl', function ($scope, $sce, static_client_factory) {

    function makeCopy(newElement) {
        var copy = {};
        jQuery.extend(true, copy, newElement);
        return copy;
    }

    function generate_client_credentials_success_callback(data, status, headers, config) {
        alert("New client credentials has successfully benn generated. \nclient_id: " + data['client_id'] + "\nclient_secret: " + data['client_secret'])
    }

    function error_callback(data, status, headers, config) {
        alert("ERROR: " +  data.ExceptionMessage);
    }

    $scope.redirect_uris = [];
    $scope.new_redirect_uri = {'value': ''};

    $scope.add_redirect_uri = function () {
        $scope.redirect_uris.splice(0, 0, makeCopy($scope.new_redirect_uri))
        $scope.new_redirect_uri = {'value': ''}
    };

    $scope.remove_redirect_uri = function (index) {
        $scope.redirect_uris.splice(index, 1);
    };

    function convert_to_simple_list(list){
        var redirect_uris = [];
        for (var i=0; i < list.length; i++){
            redirect_uris.push(list[i].value)
        }
        return redirect_uris;
    };

    $scope.generate_client_credentials = function () {
        var redirect_uris = convert_to_simple_list($scope.redirect_uris);
        static_client_factory.generate_client_credentials(redirect_uris).success(generate_client_credentials_success_callback).error(error_callback);
    };

});
