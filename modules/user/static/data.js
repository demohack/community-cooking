class User {
    constructor(py_data) {
        this.base_url = "http://127.0.0.1:5000";
        this.user_id = py_data.user.user_id;
        this.username = py_data.user.username;
        this.session_hash = py_data.user_session.session_hash;
        this.messages_from = py_data.messages_from;
        this.reacts_from = py_data.reacts_from;
        this.py_data = py_data

        let c = null;
        let r = null;

        let messages_map = new Map();
        py_data.messages_from.forEach(function(item) {
            c = _.cloneDeep(item);
            messages_map.set(c.post_id, c);
        })

        let reacts_map = new Map();
        py_data.reacts_from.forEach(function(item) {
            c = _.cloneDeep(item);

            if (reacts_map.has(c.post_id)) {
                r = reacts_map.get(c.post_id);
            } else {
                r = new Map();
                reacts_map.set(c.post_id, r);
            }

            r.set(c.user_id, c);
        })

        this.messages_from_map = messages_map;
        this.reacts_from_map = reacts_map;
    }

    async add_user_react(post_id, react) {
        const url = `${this.base_url}/user/api/react/add`;
        const method = "POST";
        const data = {
            token: this.session_hash,
            post_id: post_id,
            react: react
        };

        const response = await axios({
            url,
            method,
            data
        }).then(res => {
            console.log("post favorite story succeeded");
            res.data.reacts
            this.reacts_from.push
            //   this.favorites.set(story.storyId, story);

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

    async delete_user_react(user_id, post_id) {
        const url = `${BASE_URL}/users/${user_id}/favorites/${post_id}`;
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

            //   this.favorites.delete(storyId);
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