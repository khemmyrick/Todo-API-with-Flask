'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo) {
  $scope.deleteTodo = function(todo, index) {
    $scope.todos.splice(index, 1);
    todo.$delete();
	console.log('Deleted.');
  };
  
  $scope.saveTodos = function() {
    var filteredTodos = $scope.todos.filter(function(todo){
      if(todo.edited) {
		console.log('Returning: ', todo.name);
        return todo;
      };
    });
    filteredTodos.forEach(function(todo) {
      if (todo.id) {
        todo.$update();
		console.log('Updating todo.');
      } else {
        todo.$save();
		console.log('Saving todo.');
      }

    });
  }; 
});