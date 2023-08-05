"use strict"

class TodoList {
    constructor() {
        //
        // TodoList CLASS DATA
        //
        this.lastVisitedDate = null;
        this.firstItemID = null;
        this.nextItemID = null;

        this.firstItem = null; // pointer to the first todo item in linked list

    }

    init() {
        this.element = document.querySelector("#todoList");
        this.element.addEventListener("click", todoList_onClick);

        // check if this is the first time for the visitor
        this.restore();
        console.log(`initTodoList: repeat visit: ${this.lastVisitedDate}`);
    }

    store() {
        let date = new Date();
        this.lastVisitedDate = date.toString();
        localStorage.setItem('lastVisitedDate', this.lastVisitedDate);
        localStorage.setItem('firstItemID', this.firstItemID);
        localStorage.setItem('nextItemID', this.nextItemID);
    }

    restore() {
        this.lastVisitedDate = localStorage.getItem('lastVisitedDate');
        this.firstItemID = localStorage.getItem('firstItemID');
        this.nextItemID = localStorage.getItem('nextItemID');

        if (this.lastVisitedDate == null) {
            this.resetTodoList();
        } else {
            let date = new Date();
            this.lastVisitedDate = date.toString();
            this.restoreTodoList();
        }
    }

    findItemByKey(key) {
        let item = this.firstItem;

        while (item != null) {
            if (item.getKey() == key) {
                return item;
            }
            item = item.nextItem;
        }

        return item;
    }

    resetTodoList() {
        let date = new Date();

        this.lastVisitedDate = date.toString();
        this.firstItemID = null;
        this.nextItemID = 1;
        this.firstItem = null;

        this.store();
    }

    restoreTodoList() {
        if (this.firstItemID == null) {
            return;
        }

        let prevItem = null;
        let todoID = this.firstItemID;
        let todoItem = this.loadTodoItem(todoID);
        this.firstItem = todoItem;

        let i = 0;

        while (todoItem != null) {
            todoItem.element = createElement(todoItem);
            todoList.element.appendChild(todoItem.element);

            prevItem = todoItem;
            todoID = todoItem.nextItemID;
            todoItem = this.loadTodoItem(todoID);
            prevItem.nextItem = todoItem;

            if (i++ > 20)
                break;
        }
    }

    loadTodoItem(todoID) {
        let todoItem = new TodoItem();
        return todoItem.restore(todoID);
    }

    saveToLocalStorage() {
        let todoItem = this.firstItem;

        while (todoItem != null) {
            todoItem.store();
            todoItem = todoItem.nextItem;
        }

        todoList.store();
    }

    addTask(task) {
        let itemID = this.nextItemID++;

        let todoItem = new TodoItem();
        todoItem.init(itemID, task);

        todoItem.nextItem = this.firstItem; // works even on the first case, when firstItem is null
        todoItem.nextItemID = this.firstItemID;

        this.firstItem = todoItem;
        this.firstItemID = itemID;

        todoItem.store();
        this.store();

        return todoItem;
    }
}

let todoList = new TodoList();
