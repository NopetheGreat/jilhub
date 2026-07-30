# ==========================================
# PART 1: Imports and Data Loading
# ==========================================
import json

try:
    with open("data.json", "r", encoding="utf-8") as f:
        videos_data = json.load(f)
except FileNotFoundError:
    print("data.json not found! Run your scraper script first.")
    exit()

# ==========================================
# PART 2: HTML Head, Variables, and CSS Styles (Root & Body)
# ==========================================
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Platform</title>
    <style>
        :root {{
            --bg-color: #0f0f0f;
            --card-bg: #1f1f1f;
            --card-hover: #2a2a2a;
            --text-main: #ffffff;
            --text-muted: #aaa;
            --accent: #ff0055;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px 20px 140px 20px;
        }}
"""

# ==========================================
# PART 3: Header, Search Bar, and Autocomplete Styles
# ==========================================
html_content += """
        header {
            max-width: 1300px;
            margin: 0 auto 20px auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        h1 {
            margin: 0;
            font-size: 1.5rem;
            letter-spacing: -0.5px;
            cursor: pointer;
        }
        .search-box-wrapper {
            position: relative;
            flex: 1;
            max-width: 450px;
        }
        .search-input-container {
            display: flex;
            background: #121212;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 30px;
            overflow: hidden;
            align-items: center;
            padding-left: 16px;
            transition: border-color 0.2s;
        }
        .search-input-container:focus-within {
            border-color: var(--accent);
        }
        .search-input {
            width: 100%;
            background: transparent;
            border: none;
            color: #fff;
            padding: 10px 8px 10px 0;
            font-size: 0.95rem;
            outline: none;
        }
        .clear-search-btn {
            background: transparent;
            border: none;
            color: #777;
            font-size: 1.1rem;
            cursor: pointer;
            padding: 0 10px;
            display: none;
            transition: color 0.2s;
        }
        .clear-search-btn:hover {
            color: #fff;
        }
        .search-btn {
            background: #222;
            border: none;
            color: #aaa;
            padding: 10px 20px;
            cursor: pointer;
            border-left: 1px solid rgba(255,255,255,0.1);
            transition: background 0.2s, color 0.2s;
        }
        .search-btn:hover {
            background: #333;
            color: #fff;
        }
        .autocomplete-dropdown {
            position: absolute;
            top: calc(100% + 6px);
            left: 0;
            width: 100%;
            background: #212121;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            z-index: 999;
            display: none;
            max-height: 300px;
            overflow-y: auto;
            opacity: 0;
            transition: opacity 0.25s ease;
        }
        .autocomplete-dropdown.show {
            display: block;
            opacity: 1;
        }
        .suggestion-item {
            padding: 10px 16px;
            font-size: 0.9rem;
            color: #ddd;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
        }
        .suggestion-item:last-child {
            border-bottom: none;
        }
        .suggestion-item:hover {
            background: #2a2a2a;
            color: #fff;
        }
"""

# ==========================================
# PART 4: Video Card Grid, Badges, and Section Header Styles
# ==========================================
html_content += """
        .section-header {
            max-width: 1300px;
            margin: 30px auto 15px auto;
            font-size: 1.15rem;
            font-weight: 600;
            color: #fff;
            border-left: 4px solid var(--accent);
            padding-left: 10px;
            display: none;
        }
        .section-header.show {
            display: block;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 24px;
            max-width: 1300px;
            margin: 0 auto 30px auto;
        }
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            display: flex;
            flex-direction: column;
            transition: transform 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
            cursor: pointer;
            border: 1px solid rgba(255,255,255,0.05);
        }
        .card:hover {
            transform: translateY(-6px);
            background: var(--card-hover);
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
            border-color: rgba(255,255,255,0.15);
        }
        .thumbnail-container {
            position: relative;
            width: 100%;
            aspect-ratio: 16/9;
            background: #000;
            overflow: hidden;
        }
        .card img, .card video.preview-video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            transition: opacity 0.2s ease;
        }
        .card video.preview-video {
            opacity: 0;
            pointer-events: none;
        }
        .quality-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(4px);
            color: white;
            padding: 3px 8px;
            font-size: 0.7em;
            font-weight: 700;
            border-radius: 4px;
            letter-spacing: 0.5px;
            border: 1px solid rgba(255,255,255,0.1);
            z-index: 2;
        }
        .duration-badge {
            position: absolute;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(4px);
            color: white;
            padding: 3px 6px;
            font-size: 0.75em;
            font-weight: 600;
            border-radius: 4px;
            z-index: 2;
        }
        .content {
            padding: 14px 16px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .card h3 {
            font-size: 0.95rem;
            margin: 0 0 10px 0;
            line-height: 1.4;
            color: var(--text-main);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: auto;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.06);
        }
        .rating {
            color: #46d369;
            font-weight: 600;
        }
"""

# ==========================================
# PART 5: Pagination, Modal Layout, and Custom Video Controls Styles
# ==========================================
html_content += """
        #pagination {
            max-width: 1300px;
            margin: 20px auto 40px auto;
            display: flex;
            justify-content: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .page-btn {
            background: #1f1f1f;
            color: #ccc;
            border: 1px solid rgba(255,255,255,0.08);
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: background 0.2s, color 0.2s, border-color 0.2s;
        }
        .page-btn:hover:not(:disabled) {
            background: #2a2a2a;
            color: #fff;
            border-color: rgba(255,255,255,0.2);
        }
        .page-btn.active {
            background: #ff0055;
            color: #fff;
            border-color: #ff0055;
        }
        .page-btn:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
        #modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 20px;
            box-sizing: border-box;
            overflow-y: auto;
        }
        .modal-content {
            width: 100%;
            max-width: 1000px;
            background: #141414;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 25px 60px rgba(0,0,0,0.9);
            border: 1px solid rgba(255,255,255,0.12);
            display: flex;
            flex-direction: column;
            margin: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 22px;
            background: #181818;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .modal-header h2 {
            margin: 0;
            font-size: 1.05rem;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 85%;
            font-weight: 500;
        }
        .close-btn {
            background: rgba(255,255,255,0.08);
            border: none;
            color: #fff;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            font-size: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: background 0.2s;
        }
        .close-btn:hover {
            background: rgba(255,255,255,0.2);
        }
        .video-solid-frame {
            width: 100%;
            max-width: 800px;
            height: 450px;
            background: #000;
            margin: 0 auto;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            user-select: none;
        }
        video#modalVideoPlayer {
            width: 100%;
            height: 100%;
            object-fit: contain;
            background: #000;
            outline: none;
        }
        .custom-controls {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(transparent, rgba(0,0,0,0.85));
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 18px;
            box-sizing: border-box;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 10;
        }
        .video-solid-frame:hover .custom-controls {
            opacity: 1;
        }
        .ctrl-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            color: #fff;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 0.85rem;
            transition: background 0.2s, transform 0.2s, border-color 0.2s;
        }
        .ctrl-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
        }
        .progress-bar-container {
            flex: 1;
            height: 6px;
            background: rgba(255,255,255,0.15);
            border-radius: 3px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .progress-filled {
            height: 100%;
            background: linear-gradient(90deg, var(--accent), #ff5588);
            border-radius: 3px;
            width: 0%;
            box-shadow: 0 0 10px rgba(255, 0, 85, 0.5);
        }
        .time-display {
            font-size: 0.8rem;
            color: rgba(255,255,255,0.8);
            min-width: 85px;
            text-align: center;
            font-variant-numeric: tabular-nums;
        }
        .tap-feedback {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.6);
            color: #fff;
            padding: 10px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
            z-index: 15;
        }
        .tap-feedback.left { left: 20px; }
        .tap-feedback.right { right: 20px; }
        .tap-feedback.show { opacity: 1; }
"""
# ==========================================
# PART 6: Modal Details, Bottom Nav, and Category Styling
# ==========================================
html_content += """
        .modal-details-body {
            padding: 20px 24px;
            background: #141414;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .modal-meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.95rem;
            color: var(--text-muted);
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 14px;
        }
        .modal-rating-stats {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .share-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .share-input {
            background: #1f1f1f;
            border: 1px solid rgba(255,255,255,0.15);
            color: #fff;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            width: 260px;
            outline: none;
        }
        .copy-share-btn {
            background: var(--accent);
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.85rem;
            transition: opacity 0.2s;
        }
        .copy-share-btn:hover {
            opacity: 0.9;
        }
        .modal-suggestions-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            margin-top: 10px;
        }
        .modal-suggestions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 16px;
            max-height: 400px;
            overflow-y: auto;
            padding-right: 4px;
        }
        .modal-suggestions-grid::-webkit-scrollbar {
            width: 6px;
        }
        .modal-suggestions-grid::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 3px;
        }
        #bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #181818;
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex;
            overflow-x: auto;
            padding: 12px 16px;
            gap: 10px;
            z-index: 500;
            white-space: nowrap;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.5);
            box-sizing: border-box;
        }
        #bottom-nav::-webkit-scrollbar {
            height: 6px;
        }
        #bottom-nav::-webkit-scrollbar-thumb {
            background: #333;
            border-radius: 3px;
        }
        .cat-btn {
            background: #2a2a2a;
            color: #ccc;
            border: 1px solid rgba(255,255,255,0.05);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            transition: background 0.2s, color 0.2s, border-color 0.2s;
        }
        .cat-btn:hover, .cat-btn.active {
            background: #ff0055;
            color: #fff;
            border-color: rgba(255,255,255,0.2);
        }
    </style>
</head>
<body>
"""

# ==========================================
# PART 7: HTML Body Structure (Header, Grid, Modal Component)
# ==========================================
html_content += """
    <header>
        <h1 onclick="resetToHome()">Video Platform</h1>
        <div class="search-box-wrapper">
            <div class="search-input-container">
                <input type="text" id="searchInput" class="search-input" placeholder="Search categories or video titles..." oninput="onSearchInput()" autocomplete="off">
                <button id="clearSearchBtn" class="clear-search-btn" onclick="clearSearchInput()">&times;</button>
                <button class="search-btn" onclick="executeSearch()">🔍</button>
            </div>
            <div id="autocompleteDropdown" class="autocomplete-dropdown"></div>
        </div>
    </header>

    <div class="grid" id="video-container"></div>
    <div id="suggestedHeader" class="section-header">You might also like</div>
    <div class="grid" id="suggested-container"></div>
    <div id="pagination"></div>
    <div id="bottom-nav"></div>

    <div id="modal-overlay" onclick="closeModalOnBg(event)">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Video Title</h2>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            
            <div class="video-solid-frame" id="videoSolidFrame">
                <video id="modalVideoPlayer" autoplay oncontextmenu="return false;">
                    <source id="modalVideoSource" src="" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                
                <div class="tap-feedback left" id="tapLeftFeedback">-10s</div>
                <div class="tap-feedback right" id="tapRightFeedback">+10s</div>

                <div class="custom-controls">
                    <button class="ctrl-btn" id="playPauseBtn" onclick="togglePlayPause()" title="Play/Pause">
                        <svg id="playIconSvg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
                    </button>
                    <div class="progress-bar-container" id="progressBarContainer" onclick="seekVideo(event)">
                        <div class="progress-filled" id="progressFilled"></div>
                    </div>
                    <span class="time-display" id="timeDisplay">0:00 / 0:00</span>
                    <button class="ctrl-btn" onclick="playPreviousVideo()" title="Previous Video">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/></svg>
                    </button>
                    <button class="ctrl-btn" onclick="playNextVideo()" title="Next Video">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/></svg>
                    </button>
                    <button class="ctrl-btn" onclick="toggleFullScreen()" title="Fullscreen">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
                    </button>
                </div>
            </div>

            <div class="modal-details-body">
                <div class="modal-meta-row">
                    <div class="modal-rating-stats">
                        <span class="rating" id="modalRating">👍 0%</span>
                        <span id="modalViews">👁️ 0 views</span>
                        <span id="modalAdded">📅 2026</span>
                    </div>
                    <div class="share-container">
                        <input type="text" id="modalShareInput" class="share-input" readonly onclick="this.select()">
                        <button class="copy-share-btn" onclick="copyShareLink()">Copy Link</button>
                    </div>
                </div>

                <div class="modal-suggestions-title">Related Suggestions</div>
                <div class="modal-suggestions-grid" id="modalSuggestionsGrid"></div>
            </div>
        </div>
    </div>
"""
# ==========================================
# PART 8: JavaScript Core Setup & Rendering Engine
# ==========================================
html_content += f"""
    <script>
        const allVideos = {json.dumps(videos_data)};
        
        allVideos.forEach((v, index) => {{
            v.id = 'v' + (index + 1);
        }});

        function shuffleArray(array) {{
            for (let i = array.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }}
            return array;
        }}

        shuffleArray(allVideos);

        let currentFilteredVideos = allVideos;
        let currentPage = 1;
        const itemsPerPage = 20;
        let currentActiveVideoIndex = 0;

        function renderApp() {{
            const container = document.getElementById('video-container');
            const suggestedContainer = document.getElementById('suggested-container');
            const suggestedHeader = document.getElementById('suggestedHeader');
            
            container.innerHTML = '';
            suggestedContainer.innerHTML = '';
            suggestedHeader.classList.remove('show');

            if (currentFilteredVideos.length === 0) {{
                container.innerHTML = '<p style="text-align:center; grid-column: 1/-1; color: var(--text-muted);">No videos found.</p>';
                document.getElementById('pagination').innerHTML = '';
                return;
            }}

            const startIndex = (currentPage - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            const paginatedVideos = currentFilteredVideos.slice(startIndex, endIndex);

            paginatedVideos.forEach(video => {{
                container.appendChild(createVideoCard(video));
            }});

            if (currentPage === 1 && currentFilteredVideos.length < 8) {{
                suggestedHeader.classList.add('show');
                const shownUrls = new Set(currentFilteredVideos.map(v => v.url));
                const remainingPool = allVideos.filter(v => !shownUrls.has(v.url));
                shuffleArray(remainingPool);

                const suggestions = remainingPool.slice(0, 12);
                suggestions.forEach(video => {{
                    suggestedContainer.appendChild(createVideoCard(video));
                }});
            }}

            renderPagination();
        }}

        function createVideoCard(video) {{
            const card = document.createElement('div');
            card.className = 'card';
            
            card.innerHTML = `
                <div class="thumbnail-container">
                    <img src="${{video.thumbnail}}" alt="${{video.title}}" loading="lazy">
                    <video class="preview-video" src="${{video.url}}" muted loop preload="none"></video>
                    <span class="quality-badge">${{video.quality}}</span>
                    <span class="duration-badge">${{video.duration}}</span>
                </div>
                <div class="content">
                    <h3>${{video.title}}</h3>
                    <div class="meta">
                        <span class="rating">👍 ${{video.rating}}</span>
                        <span>👁️ ${{video.views}}</span>
                        <span>📅 ${{video.added}}</span>
                    </div>
                </div>
            `;

            const imgEl = card.querySelector('img');
            const vidEl = card.querySelector('video.preview-video');
            let hoverTimeout = null;

            card.onmouseenter = () => {{
                hoverTimeout = setTimeout(() => {{
                    vidEl.currentTime = 0;
                    vidEl.play().catch(() => {{}});
                    vidEl.style.opacity = '1';
                    imgEl.style.opacity = '0';
                }}, 400);
            }};

            card.onmouseleave = () => {{
                clearTimeout(hoverTimeout);
                vidEl.pause();
                vidEl.style.opacity = '0';
                imgEl.style.opacity = '1';
            }};

            card.onclick = () => {{
                const foundIndex = currentFilteredVideos.findIndex(v => v.id === video.id);
                currentActiveVideoIndex = foundIndex !== -1 ? foundIndex : 0;
                openVideoModal(video);
            }};

            return card;
        }}
"""

# ==========================================
# PART 9: JavaScript Player Actions, Gestures, and Controls
# ==========================================
html_content += """
        function openVideoModal(video) {
            document.getElementById('modalTitle').innerText = video.title;
            document.getElementById('modalRating').innerText = '👍 ' + video.rating;
            document.getElementById('modalViews').innerText = '👁️ ' + video.views;
            document.getElementById('modalAdded').innerText = '📅 ' + video.added;
            
            const shareUrl = window.location.origin + window.location.pathname + '?v=' + video.id;
            document.getElementById('modalShareInput').value = shareUrl;

            const player = document.getElementById('modalVideoPlayer');
            const source = document.getElementById('modalVideoSource');
            
            source.src = video.url;
            player.load();
            player.play().catch(() => {});
            
            const playIconSvg = document.getElementById('playIconSvg');
            playIconSvg.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>'; // Pause symbol
            
            document.getElementById('modal-overlay').style.display = 'flex';
            document.body.style.overflow = 'hidden';

            const modalSuggestionsGrid = document.getElementById('modalSuggestionsGrid');
            modalSuggestionsGrid.innerHTML = '';
            
            const remainingPool = allVideos.filter(v => v.id !== video.id);
            shuffleArray(remainingPool);
            remainingPool.slice(0, 8).forEach(sVideo => {
                modalSuggestionsGrid.appendChild(createVideoCard(sVideo));
            });

            window.history.pushState({videoId: video.id}, '', '?v=' + video.id);
        }

        function closeModal() {
            const player = document.getElementById('modalVideoPlayer');
            player.pause();
            document.getElementById('modal-overlay').style.display = 'none';
            document.body.style.overflow = 'auto';
            window.history.pushState({}, '', window.location.pathname);
        }

        function closeModalOnBg(event) {
            if (event.target.id === 'modal-overlay') {
                closeModal();
            }
        }

        const player = document.getElementById('modalVideoPlayer');
        
        player.addEventListener('timeupdate', () => {
            if (!isNaN(player.duration)) {
                const percent = (player.currentTime / player.duration) * 100;
                document.getElementById('progressFilled').style.width = percent + '%';
                document.getElementById('timeDisplay').innerText = formatTime(player.currentTime) + ' / ' + formatTime(player.duration);
            }
        });

        function formatTime(seconds) {
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return m + ':' + (s < 10 ? '0' : '') + s;
        }

        function togglePlayPause() {
            const playIconSvg = document.getElementById('playIconSvg');
            if (player.paused) {
                player.play();
                playIconSvg.innerHTML = '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
            } else {
                player.pause();
                playIconSvg.innerHTML = '<path d="M8 5v14l11-7z"/>'; // Play symbol
            }
        }

        function seekVideo(event) {
            const container = document.getElementById('progressBarContainer');
            const rect = container.getBoundingClientRect();
            const pos = (event.clientX - rect.left) / rect.width;
            player.currentTime = pos * player.duration;
        }

        function toggleFullScreen() {
            const frame = document.getElementById('videoSolidFrame');
            if (!document.fullscreenElement) {
                frame.requestFullscreen().catch(() => {});
            } else {
                document.exitFullscreen();
            }
        }

        const videoFrame = document.getElementById('videoSolidFrame');
        videoFrame.addEventListener('dblclick', (e) => {
            const rect = videoFrame.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const width = rect.width;

            if (clickX < width * 0.35) {
                player.currentTime = Math.max(0, player.currentTime - 10);
                showTapFeedback('left', '-10s');
            } else if (clickX > width * 0.65) {
                player.currentTime = Math.min(player.duration, player.currentTime + 10);
                showTapFeedback('right', '+10s');
            } else {
                toggleFullScreen();
            }
        });

        function showTapFeedback(side, text) {
            const fb = document.getElementById(side === 'left' ? 'tapLeftFeedback' : 'tapRightFeedback');
            fb.innerText = text;
            fb.classList.add('show');
            setTimeout(() => {
                fb.classList.remove('show');
            }, 600);
        }

        function playNextVideo() {
            if (currentFilteredVideos.length === 0) return;
            currentActiveVideoIndex = (currentActiveVideoIndex + 1) % currentFilteredVideos.length;
            openVideoModal(currentFilteredVideos[currentActiveVideoIndex]);
        }

        function playPreviousVideo() {
            if (currentFilteredVideos.length === 0) return;
            currentActiveVideoIndex = (currentActiveVideoIndex - 1 + currentFilteredVideos.length) % currentFilteredVideos.length;
            openVideoModal(currentFilteredVideos[currentActiveVideoIndex]);
        }
"""
# ==========================================
# PART 10: JavaScript Pagination, Search System, and Initialization
# ==========================================
html_content += """
        function copyShareLink() {
            const input = document.getElementById('modalShareInput');
            input.select();
            input.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(input.value);
            
            const btn = document.querySelector('.copy-share-btn');
            const originalText = btn.innerText;
            btn.innerText = 'Copied!';
            setTimeout(() => { btn.innerText = originalText; }, 2000);
        }

        function renderPagination() {
            const paginationContainer = document.getElementById('pagination');
            paginationContainer.innerHTML = '';

            const totalPages = Math.ceil(currentFilteredVideos.length / itemsPerPage);
            if (totalPages <= 1) return;

            const prevBtn = document.createElement('button');
            prevBtn.className = 'page-btn';
            prevBtn.textContent = '« Prev';
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => {
                if (currentPage > 1) {
                    currentPage--;
                    renderApp();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            };
            paginationContainer.appendChild(prevBtn);

            for (let i = 1; i <= totalPages; i++) {
                if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
                    const pageBtn = document.createElement('button');
                    pageBtn.className = i === currentPage ? 'page-btn active' : 'page-btn';
                    pageBtn.textContent = i;
                    pageBtn.onclick = () => {
                        currentPage = i;
                        renderApp();
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    };
                    paginationContainer.appendChild(pageBtn);
                } else if (i === currentPage - 3 || i === currentPage + 3) {
                    const span = document.createElement('span');
                    span.style.color = '#777';
                    span.style.padding = '8px 4px';
                    span.textContent = '...';
                    paginationContainer.appendChild(span);
                }
            }

            const nextBtn = document.createElement('button');
            nextBtn.className = 'page-btn';
            nextBtn.textContent = 'Next »';
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    renderApp();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            };
            paginationContainer.appendChild(nextBtn);
        }

        const allCategories = ["All", ...new Set(allVideos.map(v => v.category))];

        function buildCategories() {
            const nav = document.getElementById('bottom-nav');
            nav.innerHTML = '';

            allCategories.forEach((cat, index) => {
                const btn = document.createElement('button');
                btn.className = index === 0 ? 'cat-btn active' : 'cat-btn';
                btn.textContent = cat;
                btn.onclick = (e) => {
                    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    
                    currentPage = 1; 
                    if (cat === "All") {
                        currentFilteredVideos = allVideos;
                    } else {
                        currentFilteredVideos = allVideos.filter(v => v.category === cat);
                    }
                    renderApp();
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                };
                nav.appendChild(btn);
            });
        }

        function onSearchInput() {
            const input = document.getElementById('searchInput');
            const query = input.value.trim().toLowerCase();
            const clearBtn = document.getElementById('clearSearchBtn');
            const dropdown = document.getElementById('autocompleteDropdown');
            dropdown.innerHTML = '';

            if (query.length > 0) {
                clearBtn.style.display = 'block';
            } else {
                clearBtn.style.display = 'none';
                dropdown.classList.remove('show');
                return;
            }

            const matchedCategories = allCategories.filter(c => c.toLowerCase().includes(query));
            const matchedVideos = allVideos.filter(v => v.title.toLowerCase().includes(query)).slice(0, 5);

            let hasMatches = false;

            matchedCategories.forEach(cat => {
                hasMatches = true;
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.innerHTML = `📁 <span>${cat}</span>`;
                div.onclick = () => {
                    input.value = cat;
                    clearBtn.style.display = 'block';
                    dropdown.classList.remove('show');
                    filterByCategory(cat);
                };
                dropdown.appendChild(div);
            });

            matchedVideos.forEach(v => {
                hasMatches = true;
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.innerHTML = `🎬 <span>${v.title}</span>`;
                div.onclick = () => {
                    input.value = v.title;
                    clearBtn.style.display = 'block';
                    dropdown.classList.remove('show');
                    executeSearch();
                };
                dropdown.appendChild(div);
            });

            if (hasMatches) {
                dropdown.classList.add('show');
            } else {
                dropdown.classList.remove('show');
            }
        }

        function clearSearchInput() {
            const input = document.getElementById('searchInput');
            input.value = '';
            document.getElementById('clearSearchBtn').style.display = 'none';
            document.getElementById('autocompleteDropdown').classList.remove('show');
            executeSearch();
        }

        function filterByCategory(catName) {
            currentPage = 1;
            if (catName === "All") {
                currentFilteredVideos = allVideos;
            } else {
                currentFilteredVideos = allVideos.filter(v => v.category.toLowerCase() === catName.toLowerCase());
            }
            
            document.querySelectorAll('.cat-btn').forEach(b => {
                if (b.textContent.toLowerCase() === catName.toLowerCase()) {
                    b.classList.add('active');
                } else {
                    b.classList.remove('active');
                }
            });

            renderApp();
        }

        function executeSearch() {
            const query = document.getElementById('searchInput').value.trim().toLowerCase();
            document.getElementById('autocompleteDropdown').classList.remove('show');
            
            currentPage = 1;
            if (query === "") {
                currentFilteredVideos = allVideos;
            } else {
                currentFilteredVideos = allVideos.filter(v => 
                    v.title.toLowerCase().includes(query) || 
                    v.category.toLowerCase().includes(query)
                );
            }
            renderApp();
        }

        function resetToHome() {
            document.getElementById('searchInput').value = '';
            document.getElementById('clearSearchBtn').style.display = 'none';
            currentFilteredVideos = allVideos;
            currentPage = 1;
            buildCategories();
            renderApp();
            window.history.pushState({}, '', window.location.pathname);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        document.getElementById('modalVideoPlayer').addEventListener('keydown', (e) => {
            if (e.ctrlKey && (e.key === 's' || e.key === 'S')) {
                e.preventDefault();
            }
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-box-wrapper')) {
                document.getElementById('autocompleteDropdown').classList.remove('show');
            }
        });

        buildCategories();
        renderApp();

        window.addEventListener('DOMContentLoaded', () => {
            const urlParams = new URLSearchParams(window.location.search);
            const videoIdParam = urlParams.get('v');
            if (videoIdParam) {
                const targetVideo = allVideos.find(v => v.id === videoIdParam);
                if (targetVideo) {
                    openVideoModal(targetVideo);
                }
            }
        });
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully generated index.html!")