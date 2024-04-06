function showReactions(postId) {
    var reactionOptions = document.getElementById('reaction-options-' + postId);
    reactionOptions.classList.remove('hidden');
}

function hideReactions(postId) {
    var reactionOptions = document.getElementById('reaction-options-' + postId);
    reactionOptions.classList.add('hidden');
}

function handleReaction(reaction, post_id) {
    var queryToSelect = '.reaction-button span#post-' + post_id;
    var reactionButton = document.querySelector(queryToSelect);
    var emoji = '';
    var emojiColor = '';
    switch (reaction) {
        case 'Like':
            emoji = '👍';
            emojiColor = 'blue';
            break;
        case 'Love':
            emoji = '❤️';
            emojiColor = 'pink';
            break;
        case 'Haha':
            emoji = '😂';
            emojiColor = 'yellow';
            break;
        case 'Wow':
            emoji = '😮';
            emojiColor = 'orange';
            break;
        case 'Sad':
            emoji = '😢';
            emojiColor = '#FFA500'
            break;
        case 'Angry':
            emoji = '😠';
            emojiColor = 'red';
            break;
        default:
            break;
    }
    reactionButton.textContent = emoji + reaction;
    reactionButton.style.color = emojiColor;
}

$(document).ready(function(){
    $('.reaction-option').click(function(e){
        var userId = $(this).data('user-id');
        var postId = $(this).data('post-id');
        var reaction = $(this).data('reaction');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'api/save_reaction/',
            data: {
                'user_id': userId,
                'post_id': postId,
                'reaction': reaction,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            }
        });
    });
});

$(document).ready(function(){
    $('.btn.share-button').click(function(e){
        var userId = $(this).data('user-id');
        var postId = $(this).data('post-id');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'api/share_post/',
            data: {
                'user_id': userId,
                'post_id': postId,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            }
        });
    });
});

$(document).ready(function(){
    $('.notification-instance').click(function(e){
        var notificationId = $(this).data('notification-id');

        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/api/check_notification/',
            data: {
                'notification_id': notificationId,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            }
        });
    });
});

$(document).ready(function(){
  setTimeout(function(){
    $("#myAlert").fadeOut("slow", function(){
      $(this).remove();
    });
  }, 2000);
});

document.addEventListener('DOMContentLoaded', function() {
    var shareButton = document.querySelector('.share-button');
    var sharePrompt = document.getElementById('sharePrompt');

    shareButton.addEventListener('click', function() {
        setTimeout(function() {
            sharePrompt.style.display = 'block';
        }, 500);
        setTimeout(function() {
            sharePrompt.style.display = 'none';
        }, 2000);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var notificationInstances = document.querySelectorAll('[id^="notificationInstance-"]');
    
    notificationInstances.forEach(function(notificationInstance) {
        var notificationBadgeId = 'badge-' + notificationInstance.id;
        var notificationContentId = 'content-' + notificationInstance.id;
        var notificationBadge = document.getElementById(notificationBadgeId);
        var notificationContent = document.getElementById(notificationContentId);

        function handleMouseover() {
            notificationInstance.classList.add('list-group-item-active');
            notificationBadge.classList.remove('bg-danger');
            notificationBadge.classList.add('bg-info', 'text-dark');
            notificationBadge.innerText = 'Click to check';
        }

        function handleMouseout() {
            notificationInstance.classList.remove('list-group-item-active');
            notificationBadge.classList.add('bg-danger');
            notificationBadge.classList.remove('bg-info', 'text-dark');
            notificationBadge.innerText = '!';
        }

        notificationInstance.addEventListener('mouseover', handleMouseover);
        notificationInstance.addEventListener('mouseout', handleMouseout);

        notificationInstance.addEventListener('click', function() {
            notificationContent.classList.remove('fw-bold');
            notificationBadge.classList.remove('bg-info', 'text-dark');
            notificationBadge.classList.add('bg-success');
            notificationBadge.innerText = '✔';

            notificationInstance.removeEventListener('mouseover', handleMouseover);
            notificationInstance.removeEventListener('mouseout', handleMouseout);
        });
    });
});

$(document).ready(function(){
    $('.comment-upload-button').click(function(e){
        e.preventDefault();
        var userId = $(this).data('user-id');
        var postId = $(this).data('post-id');
        var commentContentId = "comment-upload-button-" + postId;
        var commentContent = document.getElementById(commentContentId).value;
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/api/upload_comment/',
            data: {
                'user_id': userId,
                'post_id': postId,
                'comment_content': commentContent,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            }
        });
        var userName = $(this).data('user-name');
        var username = $(this).data('username');
        var profileUrl = "/users/" + username + "/profile/"
        var avatarUrl = $(this).data('avatar-url');
        addComment(avatarUrl, profileUrl, userName, commentContent);
    });

    // Vanilla JavaScript event handler
    function addComment(avatarUrl, profileUrl, userName, commentContent) {
        var newCommentBox = document.createElement('div');
        newCommentBox.classList.add('comment');
        newCommentBox.innerHTML = `
            <div class="comment-box">
                <div class="image-wrapper">
                    <img class="rounded-circle article-img-comment" src="${avatarUrl}">
                </div>
                <div class="text-wrapper">
                    <a href="${profileUrl}">${userName}</a>
                    <br>
                    <small>${commentContent}</small>
                </div>
            </div>
        `;
        var commentGroup = document.querySelector('.comment-group');
        commentGroup.appendChild(newCommentBox);
    }
});