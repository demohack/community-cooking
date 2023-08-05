"use strict"

// purpose: encapsulate todo item information, and used to read from and write to localstorage.
class TodoItem {
    constructor() {
        this.myID = null; // long integer value of this ID
        this.nextItemID = null; // long integer value of the next ID in a linked list
        this.task = null; // string description of task
        this.done = null; // boolean is task done?
        this.element = null; // object reference to be assigned the HTML element li

        // *** might as well implement linked list since we're keeping tracking of nextID ***
        this.nextItem = null; // pointer to the next todo item
    }

    init(myID, task) {
        this.myID = myID; // long integer value of this ID
        this.task = task; // string description of task
    }

    getKey() {
        return `taskID-${this.myID}`;
    }

    remove() {
        let key = this.getKey();
        localStorage.removeItem(key);
        return;
    }

    store() {
        let key = this.getKey();

        let tmpItem = this.nextItem;
        let tmpElement = this.element;

        this.nextItem = null;
        this.element = null;

        let s = JSON.stringify(this);

        this.nextItem = tmpItem;
        this.element = tmpElement;

        localStorage.setItem(key, s);
        return;
    }

    restore(id) {
        this.myID = id;
        let s = localStorage.getItem(this.getKey());

        if (s == null) {
            return;
        }

        let temp = JSON.parse(s);

        this.nextItemID = temp.nextItemID;
        this.task = temp.task;
        this.done = temp.done;

        return this;
    }
}
