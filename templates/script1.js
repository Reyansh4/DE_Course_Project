function searchVideos() {
    // Replace this with actual logic to fetch videos from the database
    const searchQuery = document.getElementById('searchQuery').value;
    const videos = getVideosFromDatabase(searchQuery);

    // Display search results in the result panel
    displaySearchResults(videos);

    // Move the search bar to the top
    document.getElementById('searchPanel').classList.remove('search-panel-centered');
}

function displaySearchResults(videos) {
    const relatedVideosPanel = document.getElementById('relatedVideosPanel');
    relatedVideosPanel.innerHTML = ''; // Clear the related videos panel

    videos.forEach(video => {
        const videoSnippet = document.createElement('div');
        videoSnippet.className = 'video-snippet';
        videoSnippet.innerHTML = `
            <img src="${video.thumbnail}" alt="${video.title}">
            <h3>${video.title}</h3>
            <p>${video.description}</p>
        `;
        videoSnippet.addEventListener('click', () => showVideoDetails(video));
        relatedVideosPanel.appendChild(videoSnippet);
    });
}

function showVideoDetails(video) {
    // Replace this with actual logic to fetch video details from the database
    const videoDetails = getVideoDetailsFromDatabase(video.id);

    // Display video details in the current video panel
    const currentVideoPanel = document.getElementById('currentVideoPanel');
    currentVideoPanel.style.display = 'block'; // Show the current video panel
    document.getElementById('videoTitle').innerText = videoDetails.title;
    document.getElementById('currentVideoThumbnail').innerHTML = `<img src="${video.thumbnail}" alt="${videoDetails.title}">`;

    // Update the related videos panel with three related videos
    const relatedVideos = getRelatedVideosFromDatabase(video.id).slice(0, 3);
    displaySearchResults(relatedVideos);
}

// Replace these functions with actual backend API calls
function getVideosFromDatabase(query) {
    // Mock data for demonstration purposes
    return [
        { id: 1, title: 'Video 1', thumbnail: 'thumbnail1.jpg', description: 'Description for Video 1' },
        { id: 2, title: 'Video 2', thumbnail: 'thumbnail2.jpg', description: 'Description for Video 2' },
    ];
}

function getVideoDetailsFromDatabase(videoId) {
    // Mock data for demonstration purposes
    return { id: videoId, title: 'Video Title', description: 'Video Description', likeCount: 100 };
}

function getRelatedVideosFromDatabase(videoId) {
    // Mock data for demonstration purposes
    return [
        { id: 3, title: 'Related Video 1', thumbnail: 'thumbnail3.jpg', description: 'Description for Related Video 1' },
        { id: 4, title: 'Related Video 2', thumbnail: 'thumbnail4.jpg', description: 'Description for Related Video 2' },
        { id: 5, title: 'Related Video 3', thumbnail: 'thumbnail5.jpg', description: 'Description for Related Video 3' },
        { id: 6, title: 'Related Video 4', thumbnail: 'thumbnail6.jpg', description: 'Description for Related Video 4' },
    ];
}
