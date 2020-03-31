const $likesDisplay = $('.likes-display');
const $followingDisplay = $('.following-display');

const findCorrectElement = (classIdentifier, startingElement, maxDepth=4) => {
    let depth = 0;
    target = startingElement;
    while (!target.classList.contains(classIdentifier) || (depth > maxDepth)){
        target = target.parentElement;
        depth += 1;
    }
    if (target.classList.contains(classIdentifier)){
        return target
    }
}

$(document.body).on('click', '.like', async (e) => {
    e.preventDefault();
    const target = findCorrectElement('like', e.target);
    if (target){
        const messageId = target.dataset.messageId;
        const res = await axios.post(`/messages/${messageId}/like`);
        target.classList.add('unlike');
        target.classList.remove('like');
        target.innerHTML = 
        `
        <button class="btn btn-sm btn-primary">
            <i class="fa fa-star"></i> 
        </button>
        `;
        if ($likesDisplay){
            const currentLikes = parseInt($likesDisplay.text());
            $likesDisplay.text(currentLikes + 1);
        }
    }
});

$(document.body).on('click', '.unlike', async (e) => {
    e.preventDefault();
    const target = findCorrectElement('unlike', e.target);
    if (target){
        const messageId = target.dataset.messageId;
        const res = await axios.post(`/messages/${messageId}/unlike`);
        target.classList.add('like');
        target.classList.remove('unlike');
        target.innerHTML = 
        `
        <button class="btn btn-sm btn-secondary">
            <i class="fa fa-thumbs-up"></i> 
        </button>
        `;
        if ($likesDisplay){
            const currentLikes = parseInt($likesDisplay.text());
            $likesDisplay.text(currentLikes - 1);
        }
    }
});

$(document.body).on('click', '.unfollow', async (e) => {
    e.preventDefault();
    const target = findCorrectElement('unfollow', e.target);
    if (target){
        const userId = target.dataset.userId;
        const res = await axios.post(`/users/${userId}/unfollow`);
        target.classList.add('follow');
        target.classList.remove('unfollow');
        target.innerHTML = 
        `
        <button class="btn btn-sm btn-outline-primary">
            Follow 
        </button>
        `;
        if ($followingDisplay){
            const currentFollows = parseInt($followingDisplay.text());
            $followingDisplay.text(currentFollows - 1);
        }
    }
});

$(document.body).on('click', '.follow', async (e) => {
    e.preventDefault();
    const target = findCorrectElement('follow', e.target);
    if (target){
        const userId = target.dataset.userId;
        const res = await axios.post(`/users/${userId}/follow`);
        target.classList.add('unfollow');
        target.classList.remove('follow');
        target.innerHTML = 
        `
        <button class="btn btn-sm btn-primary">
            Unfollow 
        </button>
        `;
        if ($followingDisplay){
            const currentFollows = parseInt($followingDisplay.text());
            $followingDisplay.text(currentFollows + 1);
        }
    }
});