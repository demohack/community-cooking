"use strict"

class TodoUI {
    constructor() {
        //
        // UI global variables
        //
        this.controlBoard = null; // control board

        //
        // for new tasks
        //
        this.newTask = null;

        //
        // modelItem points to an LI that is used to clone new list items
        // because HTML is tricky and I'm a lazy coder
        //
        this.modelItem = null;
    }

    init() {
        this.controlBoard = document.querySelector("#controlboard");
        this.controlBoard.addEventListener("click", controlBoard_onClick);

        this.newTask = document.querySelector("#newtask");
        this.modelItem = document.querySelector("#modelItem"); // the first LI of the UL, invisible, used as a template
    }
}

let todoUI = new TodoUI();

function insertElement(child) {
    let sibling = todoList.element.children[1]; // skip modelItem, this.element.children[0]

    if (sibling != null) {
        todoList.element.insertBefore(child, sibling);
    } else {
        todoList.element.appendChild(child);
    }
}

function createElement(todoItem) {
    let listItemElement = todoUI.modelItem.cloneNode(true);
    listItemElement.id = todoItem.getKey();

    let taskElement = listItemElement.querySelector(".task");
    taskElement.innerText = todoItem.task;

    if (todoItem.done) {
        taskElement.classList.toggle("done");
    }

    return listItemElement;
}
