angular
    .module('nzbhydraApp')
    .directive('searchHistory', searchHistory);


function searchHistory() {
    return {
        templateUrl: 'static/html/directives/search-history.html',
        controller: ['$scope', '$http','$state', controller]
    };
    
    function controller($scope, $http, $state) {
        $scope.limit = 100;
        $scope.pagination = {
            current: 1
        };

        getSearchRequestsPage(1);

        $scope.pageChanged = function (newPage) {
            getSearchRequestsPage(newPage);
        };

        function getSearchRequestsPage(pageNumber) {
            $http.get("internalapi/getsearchrequests", {params: {page: pageNumber, limit: $scope.limit}}).success(function (response) {
                $scope.searchRequests = response.searchRequests;
                $scope.totalRequests = response.totalRequests;
                console.log($scope.searchRequests);
            });
        }

        $scope.openSearch = function (request) {
            var state;
            var stateParams = {};
            if (request.identifier_key == "imdbid") {
                stateParams.imdbid = request.identifier_value;
            } else if (request.identifier_key == "tvdbid" || request.identifier_key == "rid") {
                if (request.identifier_key == "rid" ) {
                    stateParams.rid = request.identifier_value;
                } else {
                    stateParams.tvdbid = request.identifier_value;
                } 
                
                if (request.season != "") {
                    stateParams.season = request.season;
                }
                if (request.episode != "") {
                    stateParams.episode = request.episode;
                }
            }
            if (request.query != "") {
                stateParams.query = request.query;
            }
            
            stateParams.category = request.category;

            console.log("Going to search state with params...");
            console.log(stateParams);
            console.log($state);
            $state.go("search", stateParams, {inherit: false});
        };


    }
}