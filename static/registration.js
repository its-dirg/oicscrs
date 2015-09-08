var app = angular.module('main', []);

app.factory('static_client_factory', function ($http) {
    return {
        generate_client_credentials: function (redirect_uris) {
            return $http.post("generate_client_credentials", {"redirect_uris": redirect_uris});
        }
    };
});

app.controller('IndexCtrl', function ($scope, $sce, static_client_factory) {

    function generate_client_credentials_success_callback(data, status, headers, config) {
        console.log(data)
        $scope.client_credentials = data;
    }

    function error_callback(data, status, headers, config) {
        alert("ERROR: " + data.ExceptionMessage);
    }

    $scope.redirect_uris = [];
    $scope.new_redirect_uri = "";
    $scope.client_credentials = null;

    $scope.add_redirect_uri = function () {
        if ($scope.redirect_uris.indexOf($scope.new_redirect_uri) == -1) {
            $scope.redirect_uris.push($scope.new_redirect_uri);
            $scope.new_redirect_uri = ""; // Reset value
        } else {
            alert($scope.new_redirect_uri + " is already added!");
        }
    };

    $scope.remove_redirect_uri = function (index) {
        $scope.redirect_uris.splice(index, 1);
    };

    $scope.generate_client_credentials = function () {
        static_client_factory.generate_client_credentials($scope.redirect_uris).success(generate_client_credentials_success_callback).error(error_callback);
    };

});
