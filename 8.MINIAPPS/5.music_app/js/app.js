/* ----------------------------------------------------
   MelodyLink - Application Orchestrator & Router (app.js)
   Coordinates SPA lifecycle, routing, events, and YouTube API.
------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  
  // --- App State Variables ---
  let activeYTPlayer = null;
  let playerQueueId = null; // Holds video ID if API loading is pending
  let isYTApiReady = false;

  // --- Element Selectors ---
  const views = {
    search: document.getElementById('view-search'),
    music: document.getElementById('view-music'),
    profile: document.getElementById('view-profile'),
    admin: document.getElementById('view-admin')
  };

  const navs = {
    search: document.getElementById('nav-search'),
    profile: document.getElementById('nav-profile'),
    admin: document.getElementById('nav-admin')
  };

  const authHeaderWrapper = document.getElementById('auth-header-wrapper');
  const authModal = document.getElementById('auth-modal');
  const settingsModal = document.getElementById('settings-modal');
  
  // Notifications elements
  const notifWrapper = document.getElementById('notif-wrapper');
  const notifToggleBtn = document.getElementById('notif-toggle-btn');
  const notifBadge = document.getElementById('notif-badge');
  const notifDropdown = document.getElementById('notif-dropdown');
  const notifListContainer = document.getElementById('notif-list-container');
  const notifClearBtn = document.getElementById('notif-clear-btn');

  // Search forms
  const headerSearchForm = document.getElementById('header-search-form');
  const headerSearchInput = document.getElementById('header-search-input');
  const mainSearchForm = document.getElementById('main-search-form');
  const mainSearchInput = document.getElementById('main-search-input');
  const tracksGrid = document.getElementById('tracks-grid');
  const popularTagsList = document.getElementById('popular-tags-list');
  const resultsHeadline = document.getElementById('results-headline');
  const resultsCount = document.getElementById('results-count');

  // --- 1. SPA ROUTING ENGINE ---
  const route = async () => {
    const hash = window.location.hash || '#search';
    
    // Parse path and query parameters
    // Format: #music?id=VIDEO_ID
    const parts = hash.split('?');
    const path = parts[0];
    const query = {};
    
    if (parts[1]) {
      parts[1].split('&').forEach(pair => {
        const [k, v] = pair.split('=');
        query[k] = decodeURIComponent(v);
      });
    }

    // Stop current YouTube video if playing
    stopActivePlayer();

    // Hide all view containers
    Object.values(views).forEach(v => v.classList.remove('active'));
    Object.values(navs).forEach(n => n.classList.remove('active'));
    closeNotifDropdown();

    // Route switching
    if (path === '#search') {
      views.search.classList.add('active');
      navs.search.classList.add('active');
      renderPopularTags();
      // If we have a query parameter from general search
      if (query.q) {
        headerSearchInput.value = query.q;
        mainSearchInput.value = query.q;
        executeSearch(query.q);
      } else {
        executeSearch(''); // Show default tracks
      }
    } 
    else if (path === '#music') {
      const musicId = query.id;
      if (!musicId) {
        window.location.hash = '#search';
        return;
      }
      views.music.classList.add('active');
      loadMusicDetailsPage(musicId);
    } 
    else if (path === '#profile') {
      const user = DB.auth.getCurrentUser();
      if (!user) {
        window.location.hash = '#search';
        openAuthModal('login');
        return;
      }
      views.profile.classList.add('active');
      navs.profile.classList.add('active');
      renderUserProfileView();
    } 
    else if (path === '#admin') {
      const user = DB.auth.getCurrentUser();
      if (!user || user.role !== 'admin') {
        window.location.hash = '#search';
        return;
      }
      views.admin.classList.add('active');
      navs.admin.classList.add('active');
      renderAdminPanelView();
    }
  };

  // Listen to routing hash changes
  window.addEventListener('hashchange', route);

  // --- 2. AUTHENTICATION & UI ADJUSTMENT ---
  const updateAuthUI = () => {
    const user = DB.auth.getCurrentUser();
    
    if (user) {
      // 1. Show Navigation Profile, Notifications Bell
      navs.profile.style.display = 'flex';
      notifWrapper.style.display = 'block';

      // 2. Show Admin Nav if user is admin
      if (user.role === 'admin') {
        navs.admin.style.display = 'flex';
      } else {
        navs.admin.style.display = 'none';
      }

      // 3. Update Header Account section with Avatar Dropdown
      authHeaderWrapper.innerHTML = `
        <div class="profile-dropdown-wrapper">
          <button class="profile-dropdown-btn" id="avatar-dropdown-trigger" aria-label="계정 메뉴">
            <img class="header-avatar" src="${user.avatar}" alt="${user.nickname}">
            <span class="header-nickname">${user.nickname}</span>
          </button>
          
          <div class="profile-dropdown-menu" id="profile-dropdown-menu">
            <div class="dropdown-user-info">
              <strong>${user.nickname}</strong>
              <small>@${user.username}</small>
            </div>
            <hr>
            <a href="#profile" class="dropdown-item">내 프로필</a>
            ${user.role === 'admin' ? `<a href="#admin" class="dropdown-item">관리자 백오피스</a>` : ''}
            <button class="dropdown-item" id="logout-action-btn">로그아웃</button>
          </div>
        </div>
      `;

      // Rebind dropdown trigger
      const avatarTrigger = document.getElementById('avatar-dropdown-trigger');
      const dropdownMenu = document.getElementById('profile-dropdown-menu');
      
      avatarTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownMenu.classList.toggle('show');
      });

      // Bind logout button
      document.getElementById('logout-action-btn').addEventListener('click', () => {
        DB.auth.logout();
        showToast('로그아웃', '정상적으로 로그아웃되었습니다.', 'info');
        updateAuthUI();
        window.location.hash = '#search';
      });

      // Populate notification lists
      updateNotificationBadge();
    } else {
      // Logged out: hide everything and display simple Login button
      navs.profile.style.display = 'none';
      navs.admin.style.display = 'none';
      notifWrapper.style.display = 'none';
      
      authHeaderWrapper.innerHTML = `
        <button class="btn btn-primary" id="header-login-btn">로그인</button>
      `;

      // Bind header login button
      document.getElementById('header-login-btn').addEventListener('click', () => {
        openAuthModal('login');
      });
    }

    // Refresh active views to update comment sections/forms
    const hash = window.location.hash || '#search';
    if (hash.startsWith('#music')) {
      const id = new URLSearchParams(hash.split('?')[1]).get('id');
      if (id) loadMusicComments(id);
    }
  };

  // Close dropdown on click outside
  document.addEventListener('click', () => {
    const dropdown = document.getElementById('profile-dropdown-menu');
    if (dropdown) dropdown.classList.remove('show');
  });

  // --- 3. MODAL CONTROLLERS ---
  const openAuthModal = (tab = 'login') => {
    authModal.classList.add('show');
    switchAuthTab(tab);
  };

  const closeAuthModal = () => {
    authModal.classList.remove('show');
    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('signup-username').value = '';
    document.getElementById('signup-nickname').value = '';
    document.getElementById('signup-password').value = '';
    document.getElementById('login-error').style.display = 'none';
    document.getElementById('signup-error').style.display = 'none';
  };

  const switchAuthTab = (tab) => {
    const loginTab = document.getElementById('tab-login');
    const signupTab = document.getElementById('tab-signup');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (tab === 'login') {
      loginTab.classList.add('active');
      signupTab.classList.remove('active');
      loginForm.classList.add('active');
      signupForm.classList.remove('active');
    } else {
      loginTab.classList.remove('active');
      signupTab.classList.add('active');
      loginForm.classList.remove('active');
      signupForm.classList.add('active');
    }
  };

  // Auth modal close trigger
  document.getElementById('auth-modal-close').addEventListener('click', closeAuthModal);
  document.getElementById('tab-login').addEventListener('click', () => switchAuthTab('login'));
  document.getElementById('tab-signup').addEventListener('click', () => switchAuthTab('signup'));

  // Auth forms submission handlers
  document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const userVal = document.getElementById('login-username').value;
    const passVal = document.getElementById('login-password').value;
    
    const res = DB.auth.login(userVal, passVal);
    if (res.success) {
      showToast('로그인 성공', `${res.user.nickname}님, 환영합니다!`, 'success');
      closeAuthModal();
      updateAuthUI();
      route();
    } else {
      const errorMsg = document.getElementById('login-error');
      errorMsg.textContent = res.message;
      errorMsg.style.display = 'block';
    }
  });

  document.getElementById('signup-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const userVal = document.getElementById('signup-username').value;
    const nickVal = document.getElementById('signup-nickname').value;
    const passVal = document.getElementById('signup-password').value;

    const res = DB.auth.signup(userVal, nickVal, passVal);
    if (res.success) {
      showToast('회원가입 완료', `${res.user.nickname}님, 환영합니다! 자동으로 로그인되었습니다.`, 'success');
      closeAuthModal();
      updateAuthUI();
      route();
    } else {
      const errorMsg = document.getElementById('signup-error');
      errorMsg.textContent = res.message;
      errorMsg.style.display = 'block';
    }
  });

  // Settings Modal controls
  const settingsBtn = document.getElementById('settings-btn');
  const settingsModalClose = document.getElementById('settings-modal-close');
  const settingsForm = document.getElementById('settings-form');

  settingsBtn.addEventListener('click', () => {
    const config = DB.settings.getSettings();
    document.getElementById('settings-api-key').value = config.apiKey || '';
    document.getElementById('settings-invidious-node').value = config.invidiousNode || 'https://invidious.private.coffee';
    document.getElementById('settings-browser-push').checked = config.browserPush || false;
    
    document.getElementById('settings-success').style.display = 'none';
    settingsModal.classList.add('show');
  });

  settingsModalClose.addEventListener('click', () => settingsModal.classList.remove('show'));

  settingsForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const key = document.getElementById('settings-api-key').value.trim();
    const node = document.getElementById('settings-invidious-node').value;
    const push = document.getElementById('settings-browser-push').checked;

    // Check push notifications permission request
    if (push && 'Notification' in window) {
      if (Notification.permission !== 'granted') {
        await Notification.requestPermission();
      }
    }

    DB.settings.saveSettings({
      apiKey: key,
      invidiousNode: node,
      browserPush: push
    });

    const successMsg = document.getElementById('settings-success');
    successMsg.style.display = 'block';
    
    setTimeout(() => {
      settingsModal.classList.remove('show');
    }, 1000);
  });

  // --- 4. MUSIC SEARCH LIFECYCLE ---
  const renderPopularTags = () => {
    const tags = DB.hashtags.getAllHashtags().slice(0, 10);
    popularTagsList.innerHTML = '';
    
    if (tags.length === 0) {
      popularTagsList.innerHTML = `<span class="text-muted" style="font-size:0.85rem;">아직 생성된 해시태그가 없습니다.</span>`;
      return;
    }

    tags.forEach(t => {
      const badge = document.createElement('span');
      badge.className = 'tag-badge';
      badge.textContent = `#${t.tag} (${t.count})`;
      badge.addEventListener('click', () => {
        const query = `#${t.tag}`;
        headerSearchInput.value = query;
        mainSearchInput.value = query;
        window.location.hash = `#search?q=${encodeURIComponent(query)}`;
      });
      popularTagsList.appendChild(badge);
    });
  };

  const executeSearch = async (query = '') => {
    tracksGrid.innerHTML = `<div class="loading-spinner"></div>`;
    resultsHeadline.textContent = query ? `'${query}' 검색 결과` : '전체 노래 목록';
    
    try {
      const tracks = await YouTubeSearch.search(query);
      tracksGrid.innerHTML = '';
      resultsCount.textContent = `${tracks.length}개 결과`;
      
      if (tracks.length === 0) {
        tracksGrid.innerHTML = `<div class="empty-notif" style="grid-column: 1 / -1; padding: 4rem 0;">검색 결과와 일치하는 노래가 없습니다.</div>`;
        return;
      }

      tracks.forEach(track => {
        const card = Components.renderMusicCard(track);
        
        // Open details view when card is clicked
        card.addEventListener('click', () => {
          window.location.hash = `#music?id=${track.id}`;
        });

        // Event delegation inside card (prevent details navigation if liking)
        // Note: Liking from grid is not currently coded, cards are strictly triggers,
        // but we handle detail triggers explicitly.
        
        tracksGrid.appendChild(card);
      });
    } catch (err) {
      console.error(err);
      tracksGrid.innerHTML = `<div class="empty-notif" style="grid-column:1/-1;">유튜브 데이터를 불러오는 도중 오류가 발생했습니다.</div>`;
    }
  };

  headerSearchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = headerSearchInput.value.trim();
    window.location.hash = `#search?q=${encodeURIComponent(q)}`;
  });

  mainSearchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = mainSearchInput.value.trim();
    headerSearchInput.value = q;
    window.location.hash = `#search?q=${encodeURIComponent(q)}`;
  });

  // --- 5. MUSIC DETAILS & YOUTUBE PLAYER ---
  const loadMusicDetailsPage = async (musicId) => {
    const track = YouTubeSearch.getCachedSong(musicId);
    
    if (!track) {
      // In case user landed directly via URL hash query, fetch details cached or fall back
      document.getElementById('detail-title').textContent = '상세 정보를 불러오고 있습니다...';
      try {
        await executeSearch(musicId); // Triggers YouTube query to fill cache
        const refetched = YouTubeSearch.getCachedSong(musicId);
        if (refetched) {
          setupMusicDetailUI(refetched);
        } else {
          document.getElementById('detail-title').textContent = '음악을 찾을 수 없습니다.';
        }
      } catch (err) {
        document.getElementById('detail-title').textContent = '불러오기 오류';
      }
    } else {
      setupMusicDetailUI(track);
    }
  };

  const setupMusicDetailUI = (track) => {
    document.getElementById('detail-title').textContent = track.title;
    document.getElementById('detail-channel').textContent = track.channelTitle;
    
    // Description text parsing and expansion
    const descText = track.description || '작성된 설명이 없습니다.';
    const descEl = document.getElementById('detail-description');
    const toggleDescBtn = document.getElementById('toggle-desc-btn');
    
    descEl.textContent = descText;
    descEl.classList.remove('expanded');
    
    // Show "Show More" button only if description text is long
    if (descText.length > 200) {
      toggleDescBtn.style.display = 'block';
      toggleDescBtn.textContent = '더보기';
    } else {
      toggleDescBtn.style.display = 'none';
    }

    // Toggle description event
    toggleDescBtn.onclick = () => {
      if (descEl.classList.toggle('expanded')) {
        toggleDescBtn.textContent = '접기';
      } else {
        toggleDescBtn.textContent = '더보기';
      }
    };

    // Render Likes Button state
    const likeBtn = document.getElementById('detail-like-btn');
    const likesVal = document.getElementById('detail-likes-count');
    
    likesVal.textContent = DB.likes.getLikesCount(track.id);
    
    if (DB.likes.isLiked(track.id)) {
      likeBtn.classList.add('liked');
    } else {
      likeBtn.classList.remove('liked');
    }

    // Like button click handler
    likeBtn.onclick = () => {
      const res = DB.likes.toggleLike(track.id, track.title, track.thumbnail);
      if (res.success) {
        if (res.liked) {
          likeBtn.classList.add('liked');
          showToast('좋아요', '내가 좋아하는 음악에 추가되었습니다.', 'success');
        } else {
          likeBtn.classList.remove('liked');
        }
        likesVal.textContent = res.likesCount;
        updateAuthUI(); // Refresh profiles if open
      } else if (res.error === 'login_required') {
        openAuthModal('login');
      }
    };

    // Render hashtags
    renderDetailHashtags(track.id);

    // Bind Add Hashtag form
    const addTagForm = document.getElementById('add-tag-form');
    const newTagInput = document.getElementById('new-tag-input');
    
    addTagForm.onsubmit = (e) => {
      e.preventDefault();
      const newTag = newTagInput.value.trim();
      
      const res = DB.hashtags.addHashtag(track.id, newTag);
      if (res.success) {
        newTagInput.value = '';
        renderDetailHashtags(track.id);
        showToast('해시태그 추가', `#${res.tag.tag} 태그가 추가되었습니다.`, 'success');
      } else {
        if (res.error === 'login_required') {
          openAuthModal('login');
        } else if (res.error === 'tag_exists') {
          showToast('오류', '이미 추가된 해시태그입니다.', 'warning');
        } else {
          showToast('오류', '해시태그 형식이 올바르지 않습니다.', 'warning');
        }
      }
    };

    // Load Youtube Player iframe
    loadYouTubePlayer(track.id);

    // Load Comments board
    loadMusicComments(track.id);
  };

  const renderDetailHashtags = (musicId) => {
    const listContainer = document.getElementById('detail-tags-list');
    listContainer.innerHTML = '';
    
    const track = YouTubeSearch.getCachedSong(musicId);
    const hashtags = DB.hashtags.getHashtags(musicId);

    const mergedTags = [
      ...(track?.defaultTags || []),
      ...hashtags.map(h => h.tag)
    ];

    if (mergedTags.length === 0) {
      listContainer.innerHTML = `<span class="text-muted" style="font-size:0.82rem;">아직 태그가 없습니다. 새로운 태그를 달아보세요!</span>`;
      return;
    }

    mergedTags.forEach(tag => {
      const badge = document.createElement('span');
      badge.className = 'tag-badge';
      badge.textContent = `#${tag}`;
      badge.addEventListener('click', () => {
        window.location.hash = `#search?q=${encodeURIComponent('#' + tag)}`;
      });
      listContainer.appendChild(badge);
    });
  };

  // --- YouTube IFrame API Player implementation ---
  const loadYouTubePlayer = (videoId) => {
    if (!isYTApiReady) {
      // API script is still asynchronous loading, stack request
      playerQueueId = videoId;
      return;
    }

    try {
      if (activeYTPlayer) {
        // Just load the new video stream inside the existing player frame
        activeYTPlayer.cueVideoById({ videoId: videoId });
      } else {
        // Initialize player wrapper
        activeYTPlayer = new YT.Player('yt-player-placeholder', {
          height: '100%',
          width: '100%',
          videoId: videoId,
          playerVars: {
            playsinline: 1,
            autoplay: 0,
            rel: 0
          },
          events: {
            'onError': (e) => {
              console.warn('YouTube Player error code:', e.data);
            }
          }
        });
      }
    } catch (e) {
      console.error('Failed to construct YouTube Player frame:', e);
      // Failover fallback embed
      document.getElementById('yt-player-placeholder').innerHTML = `
        <iframe src="https://www.youtube.com/embed/${videoId}?enablejsapi=1" allowfullscreen></iframe>
      `;
    }
  };

  const stopActivePlayer = () => {
    if (activeYTPlayer && typeof activeYTPlayer.stopVideo === 'function') {
      try {
        activeYTPlayer.stopVideo();
      } catch (err) {
        console.warn('Could not stop video player:', err);
      }
    }
  };

  // Attach global callback for standard YT API Load trigger
  window.onYouTubeIframeAPIReady = () => {
    isYTApiReady = true;
    if (playerQueueId) {
      loadYouTubePlayer(playerQueueId);
      playerQueueId = null;
    }
  };

  // --- 6. COMMENTS / SOCIAL LIFECYCLE ---
  const loadMusicComments = (musicId) => {
    const listContainer = document.getElementById('detail-comments-list');
    const formContainer = document.getElementById('detail-comment-form-container');
    const commentCountVal = document.getElementById('detail-comment-count');
    
    const user = DB.auth.getCurrentUser();
    const commentsList = DB.comments.getComments(musicId);
    
    commentCountVal.textContent = commentsList.length;

    // Render comment section shell using components.js helper
    const section = Components.renderCommentSection(musicId, user?.id);
    listContainer.innerHTML = '';
    formContainer.innerHTML = '';
    
    // Append Form and list nodes
    formContainer.appendChild(section.querySelector('.comments-form-container').firstElementChild);
    
    const renderedList = section.querySelector('.comments-list-container');
    listContainer.appendChild(renderedList);

    // Bind login trigger inside comments banner if logged out
    const commentLoginBtn = document.getElementById('comment-login-trigger');
    if (commentLoginBtn) {
      commentLoginBtn.onclick = () => openAuthModal('login');
    }

    // Bind comments main submission form if logged in
    const mainCommentForm = document.getElementById('comment-main-form');
    if (mainCommentForm) {
      mainCommentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('comment-main-input');
        const track = YouTubeSearch.getCachedSong(musicId);
        
        const res = DB.comments.addComment(musicId, track.title, input.value.trim());
        if (res.success) {
          input.value = '';
          showToast('의견 게시', '댓글 의견이 성공적으로 추가되었습니다.', 'success');
          loadMusicComments(musicId);
        } else {
          if (res.error === 'blocked') {
            showToast('경고', '이용 정지 상태이므로 댓글을 작성할 수 없습니다.', 'warning');
          }
        }
      });
    }

    // Bind event delegator for comments: delete buttons, reply forms, nested submission
    renderedList.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;

      // A. Delete Action
      if (btn.classList.contains('comment-delete-btn')) {
        const commentId = btn.getAttribute('data-comment-id');
        if (confirm('이 댓글을 삭제하시겠습니까? (대댓글이 있을 시 하위 트리도 함께 삭제됩니다)')) {
          const res = DB.comments.deleteComment(commentId);
          if (res.success) {
            showToast('댓글 삭제', '댓글을 정상적으로 삭제하였습니다.', 'info');
            loadMusicComments(musicId);
          }
        }
      }

      // B. Reply Toggle Text Area
      if (btn.classList.contains('comment-reply-trigger')) {
        const commentId = btn.getAttribute('data-comment-id');
        const replyBox = document.getElementById(`reply-container-${commentId}`);
        
        if (replyBox.style.display === 'none' || replyBox.innerHTML === '') {
          // Open reply form
          replyBox.style.display = 'block';
          replyBox.innerHTML = `
            <form class="comment-reply-submit-form" data-parent-id="${commentId}">
              <div class="comment-textarea-wrapper">
                <textarea class="reply-input-text" placeholder="대댓글 의견 작성..." required maxlength="300"></textarea>
                <div class="comment-textarea-footer" style="gap:0.5rem;">
                  <button type="button" class="btn btn-secondary btn-sm reply-cancel-btn" data-parent-id="${commentId}">취소</button>
                  <button type="submit" class="btn btn-primary btn-sm">답글 등록</button>
                </div>
              </div>
            </form>
          `;
          replyBox.querySelector('.reply-input-text').focus();
        } else {
          replyBox.style.display = 'none';
          replyBox.innerHTML = '';
        }
      }

      // C. Reply cancel button inside toggle
      if (btn.classList.contains('reply-cancel-btn')) {
        const parentId = btn.getAttribute('data-parent-id');
        const replyBox = document.getElementById(`reply-container-${parentId}`);
        replyBox.style.display = 'none';
        replyBox.innerHTML = '';
      }
    });

    // Handle replies form submissions (dynamic forms)
    renderedList.addEventListener('submit', (e) => {
      e.preventDefault();
      const form = e.target.closest('.comment-reply-submit-form');
      if (!form) return;

      const parentId = form.getAttribute('data-parent-id');
      const input = form.querySelector('.reply-input-text');
      const track = YouTubeSearch.getCachedSong(musicId);

      const res = DB.comments.addComment(musicId, track.title, input.value.trim(), parentId);
      if (res.success) {
        showToast('대댓글 게시', '답글 의견을 추가하였습니다.', 'success');
        loadMusicComments(musicId);
      } else {
        if (res.error === 'blocked') {
          showToast('경고', '이용 정지 상태이므로 답글을 작성할 수 없습니다.', 'warning');
        }
      }
    });
  };

  // --- 7. NOTIFICATION HUB (BELL TRAY & PUSH ALERTS) ---
  const updateNotificationBadge = () => {
    const list = DB.notifications.getNotifications();
    const unreadCount = list.filter(n => !n.isRead).length;
    
    if (unreadCount > 0) {
      notifBadge.textContent = unreadCount;
      notifBadge.style.display = 'block';
    } else {
      notifBadge.style.display = 'none';
    }
  };

  const renderNotificationsList = () => {
    const notifs = DB.notifications.getNotifications();
    notifListContainer.innerHTML = '';
    
    if (notifs.length === 0) {
      notifListContainer.innerHTML = `<div class="empty-notif">새 알림이 없습니다.</div>`;
      return;
    }

    notifs.forEach(n => {
      const item = document.createElement('div');
      item.className = `notif-item ${n.isRead ? '' : 'unread'}`;
      
      const senderAvatar = `https://api.dicebear.com/7.x/avataaars/svg?seed=${n.senderNickname}`;
      
      item.innerHTML = `
        <img class="notif-avatar" src="${senderAvatar}" alt="${n.senderNickname}">
        <div class="notif-content">
          <p class="notif-msg">
            <strong>${n.senderNickname}</strong>님이 내 좋아요 노래
            <span style="color:var(--accent-pink)">'${n.musicTitle}'</span>에 댓글을 달았습니다: 
            "${Components.escapeHTML(n.content)}"
          </p>
          <span class="notif-time">${Components.formatDate(n.createdAt)}</span>
        </div>
      `;

      // Click notif opens details and marks as read
      item.addEventListener('click', () => {
        DB.notifications.markAsRead(n.id);
        closeNotifDropdown();
        updateNotificationBadge();
        window.location.hash = `#music?id=${n.musicId}`;
      });

      notifListContainer.appendChild(item);
    });
  };

  const closeNotifDropdown = () => {
    notifDropdown.classList.remove('show');
  };

  notifToggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    notifDropdown.classList.toggle('show');
    if (notifDropdown.classList.contains('show')) {
      renderNotificationsList();
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('#notif-wrapper')) {
      closeNotifDropdown();
    }
  });

  notifClearBtn.addEventListener('click', () => {
    DB.notifications.markAllAsRead();
    renderNotificationsList();
    updateNotificationBadge();
    showToast('알림', '모든 알림을 읽음 처리했습니다.', 'info');
  });

  // --- 8. PROFILES PAGE EVENTS ---
  const renderUserProfileView = () => {
    const container = document.getElementById('profile-container');
    const profileNode = Components.renderUserProfile();
    
    container.innerHTML = '';
    container.appendChild(profileNode);

    // Tab switcher events
    const tabs = profileNode.querySelectorAll('.profile-tab-btn');
    const tabPanels = profileNode.querySelectorAll('.profile-tab-content');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tabPanels.forEach(p => p.classList.remove('active'));
        
        tab.classList.add('active');
        profileNode.querySelector(`#${tab.getAttribute('data-tab')}`).classList.add('active');
      });
    });

    // Bind event delegation for My comments list items
    const commentsList = profileNode.querySelector('.my-comments-list');
    if (commentsList) {
      commentsList.addEventListener('click', (e) => {
        const item = e.target.closest('.my-comment-item');
        if (item) {
          const mId = item.getAttribute('data-music-id');
          window.location.hash = `#music?id=${mId}`;
        }
      });
    }
  };

  // --- 9. ADMIN PANEL EVENTS ---
  const renderAdminPanelView = () => {
    const container = document.getElementById('admin-container');
    const adminNode = Components.renderAdminPanel();
    
    container.innerHTML = '';
    container.appendChild(adminNode);

    // Bind Block/Unblock toggle buttons
    adminNode.addEventListener('click', (e) => {
      const btn = e.target.closest('button');
      if (!btn) return;

      // Role Change Action
      if (btn.classList.contains('admin-role-toggle')) {
        const uId = btn.getAttribute('data-user-id');
        const res = DB.admin.changeUserRole(uId);
        if (res.success) {
          showToast('회원관리', '등급 변경을 완료했습니다.', 'success');
          renderAdminPanelView();
          updateAuthUI();
        }
      }

      // Block Action
      if (btn.classList.contains('admin-block-toggle')) {
        const uId = btn.getAttribute('data-user-id');
        const res = DB.admin.toggleBlockUser(uId);
        if (res.success) {
          showToast('회원관리', res.isBlocked ? '계정이 일시 정지되었습니다.' : '계정이 정지 해제되었습니다.', 'info');
          renderAdminPanelView();
          updateAuthUI();
        }
      }

      // Delete comments Dashboard
      if (btn.classList.contains('admin-delete-comment')) {
        const cId = btn.getAttribute('data-comment-id');
        if (confirm('관리자 권한으로 이 댓글을 강제 삭제하시겠습니까?')) {
          const res = DB.comments.deleteComment(cId);
          if (res.success) {
            showToast('관리자 댓글삭제', '전역 댓글이 삭제되었습니다.', 'info');
            renderAdminPanelView();
          }
        }
      }
    });
  };

  // --- 10. REAL-TIME PUSH ALERTS / LIVE TOAST SYSTEM ---
  const showToast = (title, text, type = 'info') => {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    toast.innerHTML = `
      <div class="toast-body">
        <div class="toast-title">${title}</div>
        <div class="toast-text">${text}</div>
      </div>
      <button class="toast-close" aria-label="닫기">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    `;

    // Toast Close click
    toast.querySelector('.toast-close').addEventListener('click', (e) => {
      e.stopPropagation();
      dismissToast(toast);
    });

    toastContainer.appendChild(toast);

    // Auto-remove toast after 5s
    setTimeout(() => {
      dismissToast(toast);
    }, 5000);
  };

  const dismissToast = (toastNode) => {
    if (toastNode && toastNode.parentNode) {
      toastNode.classList.add('hiding');
      toastNode.addEventListener('transitionend', () => {
        if (toastNode.parentNode) toastNode.parentNode.removeChild(toastNode);
      });
    }
  };

  // Intercept the custom notification event generated by db.js
  window.addEventListener('melodylink_push_notification', (e) => {
    const notif = e.detail;
    
    // Play custom sound or trigger Toast directly
    const title = `'${notif.musicTitle}' 소통 알림`;
    const text = `${notif.senderNickname}님: "${notif.content}"`;
    
    const toastContainer = document.getElementById('toast-container');
    const toast = Components.renderNotificationToast(notif);
    
    // Add close action
    toast.querySelector('.toast-close').addEventListener('click', (e) => {
      e.stopPropagation();
      dismissToast(toast);
    });

    // Make toast clickable to navigate to song discussion page
    toast.addEventListener('click', (ev) => {
      if (ev.target.closest('.toast-close')) return;
      DB.notifications.markAsRead(notif.id);
      dismissToast(toast);
      updateNotificationBadge();
      window.location.hash = `#music?id=${notif.musicId}`;
    });

    toastContainer.appendChild(toast);
    
    // Increment notifications badge and bell dropdown tray in real time
    updateNotificationBadge();
    if (notifDropdown.classList.contains('show')) {
      renderNotificationsList();
    }

    // Auto-close toast
    setTimeout(() => {
      dismissToast(toast);
    }, 6000);
  });

  // --- APP STARTUP INITIALIZATION ---
  const initApp = () => {
    // Determine active login state
    updateAuthUI();
    // Run Router once to render initial page matching active window hash
    route();
  };

  // Bootstrap app
  initApp();

});
