const BASE_URL = "http://127.0.0.1:5000";

/**
 * This class maintains the list of individual Story instances
 *  It also has some methods for fetching, adding, and removing stories
 */

class StoryList {
  constructor() {
    this.stories = new Map();
  }

  /**
   * This method is designed to be called to generate a new StoryList.
   *  It:
   *  - calls the API
   *  - builds an array of Story instances
   *  - makes a single StoryList instance out of that
   *  - returns the StoryList instance.*
   */

  // TODO: Note the presence of `static` keyword: this indicates that getStories
  // is **not** an instance method. Rather, it is a method that is called on the
  // class directly. Why doesn't it make sense for getStories to be an instance method?

  static async getStories() {
    // query the /stories endpoint (no auth required)
    const response = await axios.get(`${BASE_URL}/stories`);

    // turn the plain old story objects from the API into instances of the Story class
    const stories = response.data.stories.map(story => new Story(story));

    // build an instance of our own class using the new array of stories
    const storyList = new StoryList();

    if (stories) {
      stories.forEach(function (s) {
        storyList.stories.set(s.storyId, new Story(s));
      });
    }

    return storyList;
  }

  /**
   * Method to make a POST request to /stories and add the new story to the list
   * - user - the current instance of User who will post the story
   * - newStory - a new story object for the API with title, author, and url
   *
   * Returns the new story object
   */

  async addStory(user, newStory) {
    // this function returns the newly created story so it can be used in
    // the script.js file where it will be appended to the DOM
    const token = user.loginToken;
    const story = newStory;
    newStory = null;

    const response = await axios.post(`${BASE_URL}/stories`, {
      token,
      story
    }).then(res => {
      console.log("post story succeeded");

      newStory = new Story(res.data.story);
      this.stories.set(newStory.storyId, newStory);
      user.ownStories.set(newStory.storyId, newStory);

    }).catch(err => {
      console.log("post story failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return newStory;
  }

  async removeStory(user, storyId) {
    // removes a user's own story

    const url = `${BASE_URL}/stories/${storyId}`;
    const method = "DELETE";
    const data = {
      token: user.loginToken
    };

    let retval = false;

    const response = await axios({
      url,
      method,
      data
    }).then(res => {
      console.log("delete story succeeded");

      if (this.stories.has(storyId)) this.stories.delete(storyId);

      retval = true;

    }).catch(err => {
      console.log("delete story failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return retval;
  }

  // TODO: editStory()
  async editStory(user, storyId, story) {
    // removes a user's own story

    const url = `${BASE_URL}/stories/${storyId}`;
    const method = "PATCH";
    const data = {
      token: user.loginToken,
      story
    };

    let newStory = null;

    const response = await axios({
      url,
      method,
      data
    }).then(res => {
      console.log("update story succeeded");

      newStory = new Story(res.data.story);
      this.stories.set(newStory.storyId, newStory);
      user.ownStories.set(newStory.storyId, newStory);

    }).catch(err => {
      console.log("update story failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return newStory;
  }
}


/**
 * The User class to primarily represent the current user.
 *  There are helper methods to signup (create), login, and getLoggedInUser
 */

class User {
  constructor(userObj) {
    this.username = userObj.username;
    this.name = userObj.name;
    this.createdAt = userObj.createdAt;
    this.updatedAt = userObj.updatedAt;

    // these are all set to defaults, not passed in by the constructor
    this.loginToken = "";
    this.favorites = new Map();
    this.ownStories = new Map();
  }


  /* Login in user and return user instance.

   * - username: an existing user's username
   * - password: an existing user's password
   */

  static async login(username, password) {
    let existingUser = null;

    const response = await axios.post(`${BASE_URL}/api/login`, {
      user: {
        username,
        password
      }
    }).then(res => {
      console.log("login succeeded");

      // build a new User instance from the API response
      existingUser = new User(res.data.user);

      // on login, we want to instantiate Story instances for the user's favorites and ownStories

      res.data.user.favorites.forEach(function (s) {
        existingUser.favorites.set(s.storyId, new Story(s));
      });

      res.data.user.stories.forEach(function (s) {
        existingUser.ownStories.set(s.storyId, new Story(s));
      });

      // attach the token to the newUser instance for convenience
      existingUser.loginToken = res.data.token;
    }).catch(err => {
      console.log("login failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
        showLoginError();
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return existingUser;
  }


  /** Get user instance for the logged-in-user.
   *
   * This function uses the token & username to make an API request to get details
   *   about the user. Then it creates an instance of user with that info.
   */

  static async getLoggedInUser(token, username) {
    // if we don't have user info, return null
    if (!token || !username) return null;

    // call the API
    const response = await axios.get(`${BASE_URL}/users/${username}`, {
      params: {
        token
      }
    });

    // instantiate the user from the API information
    const existingUser = new User(response.data.user);

    // attach the token to the newUser instance for convenience
    existingUser.loginToken = token;

    // instantiate Story instances for the user's favorites, store in hashmap
    response.data.user.favorites.forEach(function (s) {
      existingUser.favorites.set(s.storyId, new Story(s));
    });

    // instantiate Story instances for the user's ownStories
    response.data.user.stories.forEach(function (s) {
      existingUser.ownStories.set(s.storyId, new Story(s));
    });

    return existingUser;
  }


  async addFavorite(story) {
    const url = `${BASE_URL}/users/${this.username}/favorites/${story.storyId}`;
    const method = "POST";
    const data = {
      token: this.loginToken
    };

    const response = await axios({
      url,
      method,
      data
    }).then(res => {
      console.log("post favorite story succeeded");

      this.favorites.set(story.storyId, story);

    }).catch(err => {
      console.log("post favorite story failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return this;
  }

  async removeFavorite(storyId) {
    const url = `${BASE_URL}/users/${this.username}/favorites/${storyId}`;
    const method = "DELETE";
    const data = {
      token: this.loginToken
    };

    let retval = false;

    const response = await axios({
      url,
      method,
      data
    }).then(res => {
      console.log("delete favorite story succeeded");

      this.favorites.delete(storyId);
      retval = true;

    }).catch(err => {
      console.log("delete favorite story failed: ", err);
      if (err.response) {
        console.log("client received an error response (5xx, 4xx): ", err.response.status);
        // client received an error response (5xx, 4xx)
      } else if (err.request) {
        console.log("client never received a response, or request never left");
        // client never received a response, or request never left
      } else {
        console.log("other error");
        // anything else
      }
    });

    return this;
  }
}

/**
 * Class to represent a single story.
 */

class Story {

  /**
   * The constructor is designed to take an object for better readability / flexibility
   * - storyObj: an object that has story properties in it
   */

  constructor(storyObj) {
    this.author = storyObj.author;
    this.title = storyObj.title;
    this.url = storyObj.url;
    this.username = storyObj.username;
    this.storyId = storyObj.storyId;
    this.createdAt = storyObj.createdAt;
    this.updatedAt = storyObj.updatedAt;
  }

  // TODO: delete() - delete user

  // TODO: edit() - edit user information
}