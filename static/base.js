// loadUserSession() loads the global object named py_data

function loadUserSession() {
    // decode base 64 encoded data passed in from python / flask to initialize frontend javascript app
    var raw_data = $("#encoded-data").text().trim(); // get the data that's embedded in a div, and need any white space to be trimmed
    var b64_data = raw_data.substring(2, raw_data.length - 1)  // need to remove the quotation marks b' and ' 
    var decoded_data = atob(b64_data);  // javascript atob decodes a string of base64 encoded data
    var py_data = decoded_data == '' ? null : JSON.parse(decoded_data);  // now the json string can be parsed and converted to a javascript object

    if (py_data) {
        if (py_data.user && py_data.user_session) {
            var menu_login = $("#menu-login");
            menu_login.text(`${py_data.user.username}`)
            menu_login.attr("href", `/user/${py_data.user.username}`)

            var menu_signup = $("#menu-signup");
            menu_signup.text("logout")
            menu_signup.attr("href", `/logout`)

            let $menu_items = $('.auth')
            $menu_items.each(function(i) {
                toggle_class($(this), enable=true);
            })
        } else {
            var menu_login = $("#menu-login");
            menu_login.text('login')
            menu_login.attr("href", '/login')

            var menu_signup = $("#menu-signup");
            menu_signup.text("signup")
            menu_signup.attr("href", `/signup`)

            let $menu_items = $('.auth')
            $menu_items.each(function(i) {
                toggle_class($(this), enable=false);
            })
        }
    }

    return py_data;
}

// https://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format
function string_format(format) {
    var args = Array.prototype.slice.call(arguments, 1);
    return format.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined' ? args[number] : match;
    });
};

function date_format(date) {
    let d = date.getDate();
    let m = date.getMonth() + 1;    // javascript oddity getMonth is 0-based
    let y = date.getFullYear();
    let hr = date.getHours();
    let min = date.getMinutes();
    return `${m}/${d}/${y} ${hr}:${min}`;
}

// toggle_class relies on jQuery
function toggle_class($elem, enable) {
    var has_class = $elem.hasClass("disabled");
    if ((enable && has_class) || (!enable && !has_class)) {
        $elem.toggleClass("disabled");
    }
}


/** loadFavicon()
 *
 * load the favicon.ico
 *
 */
 function loadFavicon(url) {
    var head = document.getElementsByTagName('head')[0];
    var link = document.createElement('link');

    // set the attributes for link element
    link.rel = "shortcut icon";
    link.href = url;

    // Append link element to HTML head
    head.appendChild(link);
};

/** loadCSS()
 *
 * load additional CSS file
 *
 * reference: https://www.geeksforgeeks.org/how-to-load-css-files-using-javascript/
 */
function loadCSS(url) {
    var head = document.getElementsByTagName('head')[0];
    var link = document.createElement('link');

    // set the attributes for link element
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = url;

    // Append link element to HTML head
    head.appendChild(link);
};

/** loadJS()
 *
 * load additional javascript file given url, and exec function runOnLoad
 *
 * reference: https://stackoverflow.com/questions/14521108/dynamically-load-js-inside-js
 */
function loadJS(url, runOnLoad) {
    let body = document.body;
    let script = document.createElement('script');
    script.src = url;

    if (runOnLoad) {
        script.onload = runOnLoad;
        script.onreadystatechange = runOnLoad;
    }

    body.appendChild(script);
};

//
// YUTE: This nifty javascript allows us to break up the main index HTML page and pop them in place based on the presense of w3-include-html tage and file name.
//

function includeHTML() {
    var z, i, elmnt, file, xhttp;
    /* Loop through a collection of all HTML elements: */
    // YUTE: performance mod: switch to use of querySelectorAll for the particular attribute

    // z = document.getElementsByTagName("*");
    z = document.querySelectorAll("[w3-include-html]");

    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        /*search for elements with a certain atrribute:*/
        file = elmnt.getAttribute("w3-include-html");
        if (file) {
            /* Make an HTTP request using the attribute value as the file name: */
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        elmnt.innerHTML = this.responseText;
                    }
                    if (this.status == 404) {
                        elmnt.innerHTML = "Page not found.";
                    }
                    /* Remove the attribute, and call this function once more: */
                    elmnt.removeAttribute("w3-include-html");
                    includeHTML();
                }
            }
            xhttp.open("GET", file, true);
            xhttp.send();
            /* Exit the function: */
            return;
        }
    }
};

