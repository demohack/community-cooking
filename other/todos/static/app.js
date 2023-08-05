"use strict"
// PROJECT: TodoList
//
// implement a todo list with add, done, delete, save, restore
//
// additional functionality:
//      due date, urgency
//      allow user to reprioritize: move taks up and down

//
// on load, construct the UI, initialize the DOM events, load the app state, restore todo list if any
//
window.addEventListener("load", function (e) {
    console.log(`window.onLoad: start h: ${document.body.clientHeight} w: ${document.body.clientWidth}`)

    todoUI.init();
    todoList.init();

    console.log('window.onLoad: page is fully loaded');
});

function controlBoard_onClick(e) {
    e.preventDefault();
    let target = e.target;

    if (target.matches("#addTask")) {
        controlBoard_addTask(target);
    } else if (target.matches("#saveList")) {
        controlBoard_saveList(target);
    } else if (target.matches("#resetList")) {
        controlBoard_resetList(target);
    }
}

function controlBoard_saveList(target) {
    todoList.saveToLocalStorage();
}

function controlBoard_resetList(target) {
    let tries = 0;

    let recursive = function (todoItem) {
        if (tries > 20)
            return;

        if (todoItem == null) {
            return;
        } else {
            recursive(todoItem.nextItem);
            if (todoItem.element) {
                todoList.element.removeChild(todoItem.element);
            }
        }
    }

    recursive(todoList.firstItem);

    todoList.resetTodoList();
}

function controlBoard_addTask(target) {
    let task = todoUI.newTask.value;

    let todoItem = todoList.addTask(task);
    todoItem.element = createElement(todoItem);
    insertElement(todoItem.element);
}

function todoList_onClick(e) {
    e.preventDefault;
    let target = e.target;

    if (target.matches("input[type='submit']")) {
        if (target.value == "+") {
            todoList_moveItemUp(target);
        } else if (target.value == "-") {
            todoList_moveItemDown(target);
        } else if (target.value == "x") {
            todoList_deleteItem(target);
        }
    } else if (target.matches("a.task")) {
        todoList_toggleItem(target);
    }
}

function todoList_moveItemUp(target) {
    // get child to be removed, because we clicked on a button child within the LI
    let child = target.parentElement;
    // get parent, the UL of the LI
    let parent = child.parentElement;

    // get sibling of such child
    let sibling1 = child.previousElementSibling;
    if (sibling1.id == "modelItem") {
        // there's nothing to do: we're at the top of the list, as there's no prior sibling
        return;
    }
    let sibling0 = sibling1.previousElementSibling;
    let sibling2 = child.nextElementSibling;

    let sibling0Item = todoList.findItemByKey(sibling0.id);
    let sibling1Item = todoList.findItemByKey(sibling1.id);
    let childItem = todoList.findItemByKey(child.id);
    let sibling2Item = (sibling2 == null ? null : todoList.findItemByKey(sibling2.id));

    if (sibling0.id == "modelItem") {
        todoList.firstItem = childItem;
        todoList.firstItemID = childItem.myID;
        todoList.store();
    } else {
        sibling0Item.nextItem = childItem;
        sibling0Item.nextItemID = childItem.myID;
        sibling0Item.store();
    }

    childItem.nextItem = sibling1Item;
    childItem.nextItemID = (sibling1Item == null ? null : sibling1Item.myID);
    childItem.store();

    sibling1Item.nextItem = sibling2Item;
    sibling1Item.nextItemID = (sibling2Item == null ? null : sibling2Item.myID);
    sibling1Item.store();

    // remove child
    parent.removeChild(child);
    // insert child before sibling
    parent.insertBefore(child, sibling1);
}

function todoList_moveItemDown(target) {
    // get child to be removed, because we clicked on a button child within the LI
    let child = target.parentElement;
    // get parent, the UL of the LI
    let parent = child.parentElement;

    // get sibling of such child
    let sibling1 = child.previousElementSibling;
    let sibling2 = child.nextElementSibling;
    let sibling3 = (sibling2 == null ? null : sibling2.nextElementSibling);

    let sibling1Item = todoList.findItemByKey(sibling1.id);
    let childItem = todoList.findItemByKey(child.id);
    let sibling2Item = (sibling2 == null ? null : todoList.findItemByKey(sibling2.id));
    let sibling3Item = (sibling3 == null ? null : todoList.findItemByKey(sibling3.id));

    if (sibling2 == null) {
        return; // last item
    }

    if (sibling1.id == "modelItem") {
        todoList.firstItem = sibling2Item;
        todoList.firstItemID = sibling2Item.myID;
        todoList.store();
    } else {
        sibling1Item.nextItem = sibling2Item;
        sibling1Item.nextItemID = sibling2Item.myID;
        sibling1Item.store();
    }

    sibling2Item.nextItem = childItem;
    sibling2Item.nextItemID = childItem.myID;
    sibling2Item.store();

    childItem.nextItem = sibling3Item;
    childItem.nextItemID = (sibling3Item == null ? null : sibling3Item.myID);
    childItem.store();

    if (sibling3 == null) {
        // swap last two items
        parent.removeChild(sibling2);
        parent.insertBefore(sibling2, child);
        return;
    } else {
        parent.removeChild(child);
        parent.insertBefore(child, sibling3);
    }
}

function todoList_deleteItem(target) {
    // get child to be removed, because we clicked on a button child within the LI
    let child = target.parentElement;
    // get parent, the UL of the LI
    let parent = child.parentElement;

    // get sibling of such child
    let sibling1 = child.previousElementSibling;
    let sibling2 = child.nextElementSibling;

    let sibling1Item = todoList.findItemByKey(sibling1.id);
    let childItem = todoList.findItemByKey(child.id);
    let sibling2Item = (sibling2 == null ? null : todoList.findItemByKey(sibling2.id));
    let sibling2ItemID = (sibling2Item == null ? null : sibling2Item.myID);

    if (sibling1.id == "modelItem") {
        todoList.firstItem = sibling2Item;
        todoList.firstItemID = sibling2ItemID;
        todoList.store();
    } else {
        sibling1Item.nextItem = sibling2Item;
        sibling1Item.nextItemID = sibling2ItemID;
        sibling1Item.store();
    }

    childItem.remove();
    parent.removeChild(child);
}

function todoList_toggleItem(target) {
    target.classList.toggle("done");
    let child = target.parentNode;

    // TODO: record the child
    let childItem = todoList.findItemByKey(child.id);
    childItem.done = target.classList.contains("done");
    childItem.store();
}
