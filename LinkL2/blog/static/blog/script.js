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
    switch (reaction) {
        case 'Like':
            emoji = '👍';
            break;
        case 'Love':
            emoji = '❤️';
            break;
        case 'Haha':
            emoji = '😂';
            break;
        case 'Wow':
            emoji = '😮';
            break;
        case 'Sad':
            emoji = '😢';
            break;
        case 'Angry':
            emoji = '😠';
            break;
        default:
            break;
    }
    reactionButton.textContent = emoji + reaction;
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

