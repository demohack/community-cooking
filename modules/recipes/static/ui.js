$(async function () {
  // cache some selectors we'll be using quite a bit
  const $allStoriesList = $("#all-articles-list");
  const $submitForm = $("#submit-form");
  const $editArticleForm = $("#edit-article-form");

  // global storyList variable
  let storyList = null;

  // global currentUser variable
  let currentUser = await checkIfLoggedIn();


  $("#nav-submit").on("click", function () {
    console.log("submit button clicked");
    $submitForm.toggle();
  });

  $("#nav-submitted").on("click", function () {
    console.log("show submitted articles");
    generateStories(currentUser, currentUser.ownStories);
  });

  $("#nav-favorites").on("click", function () {
    console.log("show favorited articles");
    generateStories(currentUser, currentUser.favorites);
  });

  /**
   * Event handler for Navigation to Homepage
   */

  $("body").on("click", "#nav-all", async function () {
    console.log("show all articles");
    storyList = await StoryList.getStories();
    generateStories(currentUser, storyList.stories);
  });

  $("#view-account-info button").on("click", function (e) {
    e.preventDefault();
    console.log("view-account-info button clicked");
    $submitForm.toggle();
    submitStory();
  });

  $("#update-account-form button").on("click", function (e) {
    e.preventDefault();
    console.log("update-account-form button clicked");
    if (updateUser()) {

    } else {
      console.log("update-account-form failed to update user");
    }
  });

  /**
   * Event handler for submitting a new story
   */

  $("#submit-form button").on("click", function (e) {
    console.log("submitted new article");
    e.preventDefault();
    $submitForm.toggle();
    submitStory();
  });

  async function submitStory() {
    // grab all the info from the form
    const title = $("#title").val();
    const author = $("#author").val();
    const url = $("#url").val();
    const username = currentUser.username;

    const storyObject = await storyList.addStory(currentUser, {
      title,
      author,
      url
    });

    $allStoriesList.prepend(generateStoryHTML(currentUser, storyObject));

    $(".button-star").on("click", async function (e) {
      await starBtnClick(e);
    });

    $(".button-star-checked").on("click", async function (e) {
      await starBtnClick(e);
    });

    $(".button-trash-true").on("click", async function (e) {
      trashBtnClick(e);
    });

    $(".button-edit-true").on("click", async function (e) {
      editBtnClick(e);
    });
  }

  /**
   * Event handler for submitting an update to a story
   */

  $("#edit-article-form button").on("click", function (e) {
    console.log("submitted update to article");
    e.preventDefault();
    $editArticleForm.toggle();
    submitUpdateStory();
  });

  async function submitUpdateStory() {
    // grab all the info from the form
    const title = $("#edit-title").val();
    const author = $("#edit-author").val();
    const url = $("#edit-url").val();
    const storyId = $("#edit-storyid").val();

    const storyObject = await storyList.editStory(currentUser, storyId, {
      title,
      author,
      url
    });

    // update the story
    $(`#${storyId} .article-author`).html(`by ${storyObject.author}`);
    $(`#${storyId} .article-title`).html(`<strong>${storyObject.title}</strong>`);
    $(`#${storyId} .article-link`).attr("href", storyObject.url);
  }

  /**
   * A rendering function to call the StoryList.getStories static method,
   *  which will generate a storyList instance. Then render it.
   */

  function generateStories(user, stories) {
    // empty out that part of the page
    $allStoriesList.empty();

    // loop through all of our stories and generate HTML for them
    stories.forEach(function (story) {
      const result = generateStoryHTML(user, story);
      $allStoriesList.append(result);
    });

    $(".button-star").on("click", async function (e) {
      await starBtnClick(e);
    });

    $(".button-star-checked").on("click", async function (e) {
      await starBtnClick(e);
    });

    $(".button-trash-true").on("click", async function (e) {
      trashBtnClick(e);
    });

    $(".button-edit-true").on("click", async function (e) {
      editBtnClick(e);
    });
  }

  /**
   * A function to render HTML for an individual Story instance
   */

  function generateStoryHTML(user, story) {
    if (!story) return;

    let hostName = getHostName(story.url);
    let starChecked = ""; //either "" or "-checked"
    let ownStory = "-false";

    if (user) {
      // check favorited hash table if storyid exists, then set starChecked to "-checked"
      if (user.favorites.has(story.storyId)) {
        starChecked = "-checked";
      }
      // check story is owned by user
      if (user.ownStories.has(story.storyId)) {
        ownStory = "-true";
      }
    }

    // render story markup
    const storyMarkup = $(`
      <li id="${story.storyId}">
        <a class="article-link" href="${story.url}" target="a_blank">
          <strong>${story.title}</strong>
        </a>
        <small class="article-author">by ${story.author}</small>
        <small class="article-hostname ${hostName}">(${hostName})</small>
        <small class="article-username">posted by ${story.username}</small>
        <button class="btn button-star${starChecked}"></button>
        <button class="btn button-trash${ownStory}"></button>
        <button class="btn button-edit${ownStory}"></button>
      </li>
    `);

    return storyMarkup;
  }


  /**
   * Event handler for clicks on stories
   */

  async function starBtnClick(e) {
    console.log("clicked on star button - at top");
    const storyId = e.target.parentElement.id;

    let button = null;
    if (!storyId) return;
    if (!storyList.stories.has(storyId)) return;
    if (!currentUser) return;

    const starChecked = currentUser.favorites.has(storyId);

    if (starChecked) {
      button = $(`#${storyId} .button-star-checked`);
      button.toggleClass("button-star-checked", false);
      button.toggleClass("button-star", true);
      currentUser.favorites.delete(storyId);
      await currentUser.removeFavorite(storyId);
    } else {
      button = $(`#${storyId} .button-star`);
      button.toggleClass("button-star-checked", true);
      button.toggleClass("button-star", false);
      currentUser.favorites.set(storyId, storyList.stories.get(storyId));
      await currentUser.addFavorite(storyList.stories.get(storyId));
    }

    console.log(`clicked on story: ${storyId}`);
  }

  async function trashBtnClick(e) {
    console.log("clicked on trash button - at top");
    const storyId = e.target.parentElement.id;
    if (!storyId) return;

    let retval = await storyList.removeStory(currentUser, storyId);
    if (retval) {
      e.target.parentElement.remove();
      if (currentUser.favorites.has(storyId)) currentUser.favorites.delete(storyId);
      if (currentUser.ownStories.has(storyId)) currentUser.ownStories.delete(storyId);
    }
  }

  async function editBtnClick(e) {
    console.log("clicked on edit button - at top");
    const storyId = e.target.parentElement.id;
    if (!storyId) return;

    // prefill the edit article form
    let story = storyList.stories.get(storyId);
    $("#edit-storyid").val(storyId);
    $("#edit-author").val(story.author);
    $("#edit-title").val(story.title);
    $("#edit-url").val(story.url);

    // show the edit article form
    $editArticleForm.show();
  }

  /**
   * On page load, checks local storage to see if the user is already logged in.
   * Renders page information accordingly.
   */

  async function checkIfLoggedIn() {
    // let's see if we're logged in
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    // if there is a token in localStorage, call User.getLoggedInUser
    //  to get an instance of User with the right details
    //  this is designed to run once, on page load
    let user = await User.getLoggedInUser(token, username);

    // get an instance of StoryList
    storyList = await StoryList.getStories();
    generateStories(user, storyList.stories);

    if (user) {
      showNavForLoggedInUser();
      updateUserInfo(user);
    }

    return user
  }


  /* hide all elements in elementsArr */

  function hideElements() {
    const elementsArr = [
      $submitForm,
      $editArticleForm,
      $allStoriesList,
      $loginForm,
      $createAccountForm
    ];
    elementsArr.forEach($elem => $elem.hide());
  }


  /* simple function to pull the hostname from a URL */

  function getHostName(url) {
    let hostName;
    if (url.indexOf("://") > -1) {
      hostName = url.split("/")[2];
    } else {
      hostName = url.split("/")[0];
    }
    if (hostName.slice(0, 4) === "www.") {
      hostName = hostName.slice(4);
    }
    return hostName;
  }

  /* sync current user information to localStorage */

  function syncCurrentUserToLocalStorage(user) {
    if (user) {
      localStorage.setItem("token", user.loginToken);
      localStorage.setItem("username", user.username);
    }
  }

});

function showLoginError() {
  $("#login-form h4").html("Login: <span class='login-error'>username or password error</span>")
}
