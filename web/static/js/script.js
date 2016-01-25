var app = angular.module('app', []);

app.factory('socket', function ($rootScope) {
  var socket = io.connect(wsUrl);
  return {
    on: function (eventName, callback) {
      socket.on(eventName, function () {
        var args = arguments;
        $rootScope.$apply(function () {
          callback.apply(socket, args);
        });
      });
    },
    emit: function (eventName, data, callback) {
      socket.emit(eventName, data, function () {
        var args = arguments;
        $rootScope.$apply(function () {
          if (callback) {
            callback.apply(socket, args);
          }
        });
      })
    }
  };
});

function MyCtrl($scope, socket) {

    $scope.drivers = [];
    $scope.race = "RACE";
    $scope.startImg = "/static/img/start.png";

    socket.on('init', function(data) {
        var obj = angular.fromJson(data);
        $scope.drivers = obj.rows;
        if (obj.start == 0) {
            $scope.race = "RACE";
            $scope.startImg = "/static/img/stop.png";
        }
        else if (obj.start == 1) {
            $scope.race = "PREPARE";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 2) {
            $scope.race = "5";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 3) {
            $scope.race = "4";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 4) {
            $scope.race = "3";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 5) {
            $scope.race = "2";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 6) {
            $scope.race = "1";
            $scope.startImg = "/static/img/start.png";
        }
        else if (obj.start == 7) {
            $scope.race = "START";
            $scope.startImg = "/static/img/start.png";
        }

    });

    $scope.start = function (data) {
        socket.emit('send:start', {
            message: data
        });
    };

    $scope.rst = function () {
        socket.emit('send:reset', {});
    };

    $scope.request = function () {
        socket.emit('send:request', {
            message: ""
        });
    };

}

window.onload = function() {
    function foo() {
        var el = document.getElementById("sc");
        var scope = angular.element(el).scope();
        scope.request();
    }
    setInterval(foo, 150);
}
