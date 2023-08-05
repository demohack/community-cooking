2020-10-31 22:49
    - Hacker News!!!
    - reading the requirements

2020-11-01 06:00
    - reread the requirements
    - downloaded the initial source code

Goals
- complete a commulative project
- make a clone of the news aggregator Hacker News, https://news.ycombinator.com/
- this exercises focuses on how to use an existing API to build out the functionality in front-end Javascript using jQuery and AJAX
- https://hackorsnoozev3.docs.apiary.io/#introduction/quickstart
- functionalities: users can create accounts, login, save articles, upload stories
- 10 to 15 hrs
- follow each step carefully and closely
- can reach out to TAs and mentors
- when finished, submit, and discuss code with mentor
- then live code review
- then share code with peers

http://curric.rithmschool.com/springboard/exercises/hack-or-snooze-ajax-api/

working copy of solution
https://hack-or-snooze.surge.sh/

code of solution
http://curric.rithmschool.com/springboard/exercises/hack-or-snooze-ajax-api/solution/index.html

### PART 0 - read the docs
https://hackorsnoozev3.docs.apiary.io/#

What is Insomnia?
https://apis.support.brightcove.com/general/use-insomnia-api-requests.html
https://dev.to/kmcknight91/how-to-use-insomnia-to-test-api-endpoints-1lad


2020-11-01 09:37
Goals!
- read the code, see what's there already, read the comments
- reread the requirements
- lay out a design plan
    = what do I want the look and feel?
    = how do I feel about the demo app?
        > don't like the color scheme
        > don't like the login/signup page design
    = what is the API capable of?
        > can we do commenting?  -no


2020-11-01 20:05
- Tried to login and failed
- implementing error handling code for axios requests
https://www.intricatecloud.io/2020/03/how-to-handle-api-errors-in-your-web-app-using-axios/

2020-11-04 07:00
- Focus on user / session, be able to login and logout

2020-11-13 07:46
- getting started again, need to assess the requirements, read the code, lay out the work that needs to be done, start writing code.

assessment of what we're starting out with:
- index.html
    - main nav bar
    - main content area for stories
    - user account
        - login
        - create account
        - user profile info

- api-classes
    - StoryList class
        - getStories
        - addStory() - TODO
        - remove() - TODO
    - User class
        - create()
        - login()
        - getLoggedInUser()
        - update() - TODO
        - remove() - TODO
    - Story class
        - add() - TODO
        - remove() - TODO
        - update() - TODO

- ui
    - loginForm.onSubmit()
    - createAccountForm.onSubmit()
    - navLogout.onSubmit()
    - navLogin.onSubmit()
    - body.onClick(#nav-all)
    - checkIfLoggedIn()
    - loginAndSubmitForm()
    - generateStories()
    - generateStoryHTML()
    - hideElements()    - hides the submitForm, allStoriesList, filteredArticles, ownStories, loginForm, createAccountForm
    - showNavForLoggedInUser()
    - getHostName()
    - syncCurrentUserToLocalStorage()

    - global variables:
        - allStoriesList
        - ownStories
        - filteredArticles
        - submitForm
        - loginForm
        - createAccountForm
        - navLogin
        - navLogout

2020-11-15 12:41 pm
Part 1 - completed
api-classes.js
    this file contains the classes you will use and
    should be where you place all the logic for communicating with the API
    make sure you understand the keyword static before moving on

ui.js
    this file makes use of the classes in api-classes.js
    contains all of the DOM manipulation and jQuery code necessary

- When a user has successfully logged in, a secured string or “token” is sent back from the server. JWT (json web token)
- We will also need this token when we make future API requests that are “Auth Required.”
- Note also that when the page refreshes, the user can stay logged in. This is because we are storing the token in localStorage!
- Make sure you read through the code and play around with it before moving on!

Part 2
- Once a user has logged in, allow them to create a new story.
    = This will involve adding a new form that when submitted will send the data in the form to the API,
      which will respond with the newly created story.

- Make sure you append the newly created story to the DOM and only allow logged in users to create a new story.
    = The method for creating a story should be defined in the StoryList class.

TODO:
x on login, update user profile info
x on login, show menu for showing submit form, submitted stories, favorite stories
x on submit story, post to server
x on submit story, refresh story

2020-11-16 07:50
Part 3: Favoriting stories
- Allow logged in users to “favorite” and “un-favorite” a story.
    = need to provide a favorite button associated with each story
    = reread the HTML to see what elements can be used, what needs to be added...
        > nothing in html
    = reread the ui.js
        > bingo: modify the generateStoryHTML()

- These stories should remain favorited when the page refreshes.
    = need to use local storage??

- Allow logged in users to see a separate list of favorited stories.
    = implement a function to respond to submitted stories menu click

- The methods for favoriting and unfavoriting a story should be defined in the User class.

2020-11-18 9:04 am

2020-11-30 8:35 am

2020-12-04 8:00 am

todo today:
- fix problem of not being able to delete own stories

2020-12-08 4:18 pm
- finally fixed the problem of not being able to delete own stories
- I was passing in an invalid token value, and error code wasn't catching it

2020-12-12 6:47 am
Fix:
x Hide the user info box. It appears regardless of state of user login: on list of stories without logging in, on login page, and after login.
- Show the user info box, and hide the stories, when the user's name is clicked
