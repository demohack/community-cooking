//Module Pattern
//https://coryrylan.com/blog/javascript-module-pattern-basics
//http://www.adequatelygood.com/JavaScript-Module-Pattern-In-Depth.html

let app_ui = (function ($) {
    var py_data = load_data_maps(loadUserSession());
    var $list_html = $("#all-articles-list");
    var curr_user = new User(py_data);

    function gen_list_html () {
        // empty out that part of the page
        $list_html.empty();

        // loop for each item in list, generate HTML and append
        py_data.messages_to.forEach(function (post_item) {
            const $item_html = gen_item_html(post_item);
            $list_html.append($item_html);
        });

        $(".button-star").on("click", async function (e) {
            await start_btn_click(e);
        });

        $(".button-star-checked").on("click", async function (e) {
            await start_btn_click(e);
        });

        $(".button-trash-true").on("click", async function (e) {
            trash_btn_click(e);
        });

        $(".button-edit-true").on("click", async function (e) {
            edit_btn_click(e);
        });
    };

    function gen_item_html (post_item) {
        if (!post_item) return;

        let star_checked_str = ""; //either "" or "-checked"
        let own_post_str = "-false";

        if (py_data) {
            if (py_data.user && py_data.messages_map && py_data.reacts_map) {

                let post_id = post_item.post_id;

                // check user reacted, then set starChecked to "-checked"
                if (py_data.reacts_map.has(post_id)) {

                    r = py_data.reacts_map.get(post_id);
                    star_checked_str = r.has(py_data.user.id) ? "-true" : "";

                } else {
                    r = new Map();
                    r = py_data.reacts_map.set(post_id, r);
                    star_checked_str = "";
                }
    
                // check story is owned by user
                if (py_data.messages_map.has(post_id)) {

                    let message = py_data.messages_map.get(post_id);

                    if (message.user_id = py_data.user.id) {
                        own_post_str = "-true";
                    }
                }
            }
        }

        // render story markup
        const $item_html = $(`
          <li id="${post_item.post_id}">
            <strong>${post_item.post_title}</strong>
            <span>${post_item.post_content}</span>
            <small class="article-from">from: ${post_item.from_name}</small>
            <small class="article-to">to: ${post_item.to_name}</small>
            <small class="article-date">date: ${date_format(new Date(post_item.post_created))}</small>
            <button class="btn button-star${star_checked_str}"></button>
            <button class="btn button-trash${own_post_str}"></button>
            <button class="btn button-edit${own_post_str}"></button>
          </li>
        `);

        return $item_html;
    }


    /**
     * Event handler for clicks on stories
     */

     const start_btn_click = async function (e) {
        console.log("clicked on star button - at top");
        const post_id = e.target.parentElement.id;

        if (!post_id || !py_data) return;
        if (!py_data.user || !py_data.messages_map || !py_data.reacts_map) return;

        let user_id = py_data.user.id;
        let reacts = null;
        let star_checked = false;

        if (py_data.reacts_map.has(post_id)) {
            reacts = py_data.reacts_map.get(post_id);
            star_checked = reacts.has(user_id);
        } else {
            reacts = new Map();
            reacts = py_data.reacts_map.set(post_id, reacts);
            star_checked = false;
        }

        let button = $(`#${post_id}`);

        if (star_checked) {
            button.toggleClass("button-star-checked", false);
            button.toggleClass("button-star", true);

            let r = await curr_user.delete_user_react(user_id, post_id);
            if (r)
                reacts.delete(user_id);
    
        } else {
            button.toggleClass("button-star-checked", true);
            button.toggleClass("button-star", false);

            let r = await curr_user.add_user_react(post_id, 'like');
            if (r)
                reacts.set(user_id, r);
        }

        console.log(`clicked on story: ${post_id}`);
    }

    const trash_btn_click = async function (e) {
        console.log("clicked on trash button - at top");
        const post_id = e.target.parentElement.id;
        if (!post_id) return;

        let retval = await storyList.removeStory(currentUser, post_id);
        if (retval) {
            e.target.parentElement.remove();
            if (favorites.has(post_id)) favorites.delete(post_id);
            if (ownStories.has(post_id)) ownStories.delete(post_id);
        }
    }

    const edit_btn_click = async function (e) {
        console.log("clicked on edit button - at top");
        const post_id = e.target.parentElement.id;
        if (!post_id) return;

        // prefill the edit article form
        let story = storyList.stories.get(post_id);
        $("#edit-storyid").val(post_id);
        $("#edit-author").val(story.author);
        $("#edit-title").val(story.title);
        $("#edit-url").val(story.url);

        // show the edit article form
        $editArticleForm.show();
    }

    function load_data_maps (py_data) {
        // purpose: creates maps of messages and reacts for faster search

        // create map of messages
        // and for each message, create map of reacts for that mesage

        // assumes reacts is sorted by post_id, react_id
        let c = null;
        let r = null;

        let messages_map = new Map();
        py_data.messages_to.forEach(function(item) {
            c = _.cloneDeep(item);
            messages_map.set(c.post_id, c);
        })

        let reacts_map = new Map();
        py_data.reacts_to.forEach(function(item) {
            c = _.cloneDeep(item);

            if (reacts_map.has(c.post_id)) {
                r = reacts_map.get(c.post_id);
            } else {
                r = new Map();
                reacts_map.set(c.post_id, r);
            }

            r.set(c.user_id, c);
        })

        py_data.messages_map = messages_map;
        py_data.reacts_map = reacts_map;

        return py_data
    }

    const init_page = function () {
        gen_list_html();
    };

    return {
        init_page: init_page
    };

})(jQuery);

$(document).ready(function () {

    app_ui.init_page();
});