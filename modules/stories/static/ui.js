//Module Pattern
//https://coryrylan.com/blog/javascript-module-pattern-basics
//http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html
console.log("#### ui.js - start");

let app_ui = (function($, sl) {

    const init_page = function() {
        console.log("#### ui.js - $(document).ready() - app_ui.init_page() - start");
        // load the stories that the logged in user can see

        sl.main();
        console.log("#### ui.js - $(document).ready() - app_ui.init_page() - end");
    };

    return {
        init_page: init_page
    };
})(jQuery, story_list);

$(document).ready(function() {
    console.log("#### ui.js - $(document).ready() - start");
    app_ui.init_page();
    console.log("#### ui.js - $(document).ready() - end");
});

console.log("#### ui.js - end");
