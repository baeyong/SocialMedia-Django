

function getPosts() {
    console.log("In the getPosts function")
    let xhr = new XMLHttpRequest() // Creating new XMLHttpRequest

    // onreadystatechange defines a function to be executed when the readystate changes
    // when it is finally ready, we will update the page
    xhr.onreadystatechange = function() {

        // readyState(0 = unsent, 1 = opened, 2 = headers rec'd, 3 = some data rec'd, 4 = response ready)
        if (this.readyState != 4) return
        // the response is ready
        updatePage(xhr,1)
    }

    // Executes an async GET request to obtain the current item list
    // Sets the request method, request URL, and synchronous flag
    xhr.open("GET", "get-global", true)
    xhr.send()
}


function getFollowerPosts() {
    console.log(" In the getFollowerPosts function")
    let xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function() {
        if (this.readyState != 4) return

        updatePage(xhr, 2)
    }

    xhr.open("GET", "get-follower", true)
    xhr.send()
}


// is called from getPosts, getFollowerPosts, getComments
function updatePage(xhr, page) {
    console.log("In the update page function")
    console.log(xhr.status)
    // status (200 = OK, 404 = not found, etc)
    if (xhr.status == 200) {
        // Results are returned in JSON
        let response = JSON.parse(xhr.responseText)
        
        updateList(response, page)
        return
    }
}

// Your JS should not delete and then recreate existing posts, existing comments, existing text boxes, and submit buttons during refresh
// Must do DUPLCATE DETECTION to recognize that a post or comment is already present and not add it again
// So look at the element ids already at the top of the page if its already there
// called in updatePage
function updateList(xhr, page) {
    console.log("in the updateList Function")
    let posts = xhr['posts'] // from the serializer in the views function
    let comments = xhr['comments']
    let list = document.getElementById("my-posts-go-here")
    if (page === 2) {
        list = document.getElementById("my-follower-posts-go-here")
    }

    for (let i = 0; i < posts.length; i++) {
        let post = posts[i]

        // create the id
        const postID = 'id_post_div_' + post.id
        let postInDom = document.getElementById(postID)

        if (!postInDom) { // if the post doesn't exist we should create it 
            // creating the post element
            let postElement = createPost(post)

            // creating the comment element 
            let commentBoxElement = commentBoxElementHelper(post)

            //createing the comment input 
            let commentInputElement = createCommentInput(post, page)

            list.prepend(postElement, commentBoxElement, commentInputElement) 

        }

    }

    // for commenting
    for (let j = 0; j < comments.length; j++) {
        let comment = comments[j]

        const commentID = 'id_comment_div_' + comment.id
        let commentInDom  = document.getElementById(commentID)

        if (!commentInDom) {
            const postCommentID = "my-comments-go-here-for-post-" + comment.post_number
            let postCommentBox = document.getElementById(postCommentID)
            
            let commentElement = commentElementHelper(comment)
            console.log("this is commentElement", commentElement)

            
            postCommentBox.prepend(commentElement)
        
        }
    }

}

// called in updateList
function createPost(post) {
    
    let postElement = document.createElement("div")
    postElement.id = "id_post_div_" + post.id
    postElement.className = "roundedPostDivs"

    // post user
    let postCreator = document.createElement("a")
    let userProfileURL = "otherprofile/" + post.user_id
    postCreator.setAttribute("href", userProfileURL) // setting up the users name to click from the post
    postCreator.id = "id_post_profile_" + post.user_id
    postCreator.innerHTML = post.user_first_name + " " + post.user_last_name

    // post text
    let postContent = document.createElement("span")
    postContent.id = "id_post_text_" + post.id
    postContent.innerHTML = post.new_post
    
    // post date and time
    let postTime = document.createElement("span")
    postTime.id = "id_post_date_time_" + post.id
    postTime.innerHTML = post.date
    postTime.className = "dateStyle"

    // adding appropriate parts to the post
    let postIntro = document.createElement("span")
    postIntro.innerHTML = "Post by "
    let dash1 = document.createElement("span")
    dash1.innerHTML = " - "
    let dash2 = document.createElement("span")
    dash2.innerHTML = " - "

    postElement.appendChild(postIntro)
    postElement.appendChild(postCreator)
    postElement.appendChild(dash1)
    postElement.appendChild(postContent)
    postElement.appendChild(dash2)
    postElement.appendChild(postTime)

    return postElement
}

function commentElementHelper(comment) {
    let commentElement = document.createElement("div")
    commentElement.id = "id_comment_div_" + comment.id
    commentElement.className = "roundedpostDivscommentIndent"

    console.log("in the commentElementHelper, this is the comment object", comment)
    let commentCreator = document.createElement("a")
    let userProfileURL = "otherprofile/" + comment.user_id
    commentCreator.setAttribute("href", userProfileURL)
    commentCreator.id = "id_comment_profile_" + comment.user_id
    commentCreator.innerHTML = comment.user_first_name + " " + comment.user_last_name

    let commentContent = document.createElement("span")
    commentContent.id = "id_comment_text_" + comment.id
    commentContent.innerHTML = comment.new_comment

    let commentTime = document.createElement("span")
    commentTime.id = "id_comment_date_time_" + comment.id
    commentTime.innerHTML = comment.date
    commentTime.className = "dateStyle"

    let commentIntro = document.createElement("span")
    commentIntro.innerHTML = "Comment by "
    let dash1 = document.createElement("span")
    dash1.innerHTML = " - "
    let dash2 = document.createElement("span")
    dash2.innerHTML = " - "

    commentElement.appendChild(commentIntro)
    commentElement.appendChild(commentCreator)
    commentElement.appendChild(dash1)
    commentElement.appendChild(commentContent)
    commentElement.appendChild(dash2)
    commentElement.appendChild(commentTime)

    return commentElement

}

function commentBoxElementHelper(post) {
    console.log("In commentBoxElementHelper function")
    let commentBoxElement = document.createElement("div")
    commentBoxElement.id = "my-comments-go-here-for-post-" + post.id

    return commentBoxElement
}

// called from onClick on the createCommentInput
// Post will be passed from createCommentInput, need to pass in
function addComment(post_id, page) {
    console.log("in the addComment function")
    let commentTextElement = document.getElementById("id_comment_input_text_" + post_id)

    let commentTextValue = commentTextElement.value

    // Clear input box and old error message
    commentTextElement.value = ""

    let xhr = new XMLHttpRequest()

    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr, page)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("item=" + commentTextValue + "&csrfmiddlewaretoken=" + getCSRFToken() + "&hiddenPostValue=" + post_id + "&page=" + page)

}

// add if its follower or global
// called from updateList
function createCommentInput(post, page) {
    let commentInputElement = document.createElement("div")
    commentInputElement.className = "id_comment_div_" + post.id
    commentInputElement.id = "commentInputStyle"

    const newLabel = document.createElement("label")
    newLabel.innerHTML = "Comment: "

    var inputBox = document.createElement("input")
    inputBox.setAttribute("type", "text")
    inputBox.id = "id_comment_input_text_" + post.id
    inputBox.setAttribute("name", "commentText")
    inputBox.className = 'inputBoxStyle'

    var submitButton = "<button id=" + "'id_comment_button_" + post.id + "'" + " onclick='addComment(" + post.id + "," + page + ")'" + ">Submit</button>"
    var x = document.createElement("span")
    x.innerHTML = submitButton

    commentInputElement.appendChild(newLabel)
    commentInputElement.appendChild(inputBox)
    commentInputElement.appendChild(x)
    
    return commentInputElement

}

function getCSRFToken() {
    console.log("in getCSRFToken function")
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}
