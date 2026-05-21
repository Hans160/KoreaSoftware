/* ----------------------------------------------------
   MelodyLink - Dynamic UI Components Renderer (components.js)
   Generates structured HTML nodes and interfaces for the SPA views.
------------------------------------------------------- */

const Components = (() => {
  
  // Custom SVG Icon Helper
  const getIcon = (name, className = '') => {
    const icons = {
      play: `<svg class="${className}" viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`,
      heart: `<svg class="${className}" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`,
      comment: `<svg class="${className}" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>`,
      trash: `<svg class="${className}" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>`,
      reply: `<svg class="${className}" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 17 4 12 9 7"></polyline><path d="M20 18v-2a4 4 0 0 0-4-4H4"></path></svg>`,
      user: `<svg class="${className}" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>`,
      shield: `<svg class="${className}" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>`,
      settings: `<svg class="${className}" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>`,
      externalLink: `<svg class="${className}" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`
    };
    return icons[name] || '';
  };

  /* --- 1. RENDER MUSIC CARD --- */
  const renderMusicCard = (track) => {
    const isLiked = DB.likes.isLiked(track.id);
    const likesCount = DB.likes.getLikesCount(track.id);
    const commentsCount = DB.comments.getComments(track.id).length;
    const hashtags = DB.hashtags.getHashtags(track.id);

    // Concat default tags with user tags
    const displayTags = [
      ...(track.defaultTags || []),
      ...hashtags.map(h => h.tag)
    ].slice(0, 4); // Limit card to 4 tags to keep clean

    const card = document.createElement('div');
    card.className = 'music-card';
    card.setAttribute('data-id', track.id);
    
    card.innerHTML = `
      <div class="music-card-thumb-wrapper">
        <img class="music-card-thumb" src="${track.thumbnail}" alt="${track.title}" loading="lazy">
        <div class="music-card-overlay">
          <div class="play-btn-circle">
            ${getIcon('play')}
          </div>
        </div>
      </div>
      <div class="music-card-content">
        <div>
          <h3 class="music-card-title">${track.title}</h3>
          <p class="music-card-channel">${track.channelTitle}</p>
          <div class="music-card-tags">
            ${displayTags.map(tag => `<span class="music-card-tag">#${tag}</span>`).join('')}
          </div>
        </div>
        <div class="music-card-footer">
          <span class="music-card-likes">
            ${getIcon('heart')}
            <span class="card-likes-val">${likesCount}</span>
          </span>
          <span class="music-card-comments">
            ${getIcon('comment')}
            <span>${commentsCount}</span>
          </span>
        </div>
      </div>
    `;

    return card;
  };

  /* --- 2. RENDER COMMENTS / DISCUSSIONS SECTION --- */
  const renderCommentSection = (musicId, currentUserId) => {
    const container = document.createElement('div');
    container.className = 'comment-section-wrapper';

    const comments = DB.comments.getComments(musicId);
    const user = DB.auth.getCurrentUser();

    // A. Comment Form Area (Header)
    let formHTML = '';
    if (user) {
      formHTML = `
        <form id="comment-main-form">
          <div class="comment-textarea-wrapper">
            <textarea id="comment-main-input" placeholder="이 음악에 대한 의견을 나누어 보세요..." maxlength="500" required></textarea>
            <div class="comment-textarea-footer">
              <button type="submit" class="btn btn-primary btn-sm">의견 등록</button>
            </div>
          </div>
        </form>
      `;
    } else {
      formHTML = `
        <div class="login-banner">
          의견을 나누고 좋아요를 누르시려면 <button class="login-banner-btn" id="comment-login-trigger">로그인</button>이 필요합니다.
        </div>
      `;
    }
    
    // B. Build Threads (Top-level and replies)
    const topLevelComments = comments.filter(c => !c.parentId);
    const repliesMap = {};
    comments.forEach(c => {
      if (c.parentId) {
        if (!repliesMap[c.parentId]) repliesMap[c.parentId] = [];
        repliesMap[c.parentId].push(c);
      }
    });

    let listHTML = '';
    if (comments.length === 0) {
      listHTML = `<div class="empty-notif" style="padding: 3rem 0;">첫 번째 의견을 남겨보세요!</div>`;
    } else {
      listHTML = topLevelComments.map(c => renderCommentNode(c, repliesMap[c.id] || [], user)).join('');
    }

    container.innerHTML = `
      <div class="comments-form-container">${formHTML}</div>
      <div class="comments-list-container" style="margin-top: 1rem;">${listHTML}</div>
    `;

    return container;
  };

  // Helper: Generates comment tree nodes (supports 1-level reply nesting for neat SNS style)
  const renderCommentNode = (comment, replies, currentUser) => {
    const isOwner = currentUser && comment.userId === currentUser.id;
    const isAdmin = currentUser && currentUser.role === 'admin';
    const canDelete = isOwner || isAdmin;
    
    const roleTag = comment.userId === 'u_admin' ? `<span class="comment-role-tag">관리자</span>` : '';
    
    const deleteBtn = canDelete 
      ? `<button class="comment-action-btn delete comment-delete-btn" data-comment-id="${comment.id}">
           ${getIcon('trash')} 삭제
         </button>` 
      : '';
      
    const replyBtn = currentUser 
      ? `<button class="comment-action-btn comment-reply-trigger" data-comment-id="${comment.id}">
           ${getIcon('reply')} 답글
         </button>`
      : '';

    let repliesHTML = '';
    if (replies.length > 0) {
      repliesHTML = `
        <div class="comment-replies">
          ${replies.map(r => {
            const rIsOwner = currentUser && r.userId === currentUser.id;
            const rCanDelete = rIsOwner || isAdmin;
            const rRoleTag = r.userId === 'u_admin' ? `<span class="comment-role-tag">관리자</span>` : '';
            const rDeleteBtn = rCanDelete 
              ? `<button class="comment-action-btn delete comment-delete-btn" data-comment-id="${r.id}">
                   ${getIcon('trash')} 삭제
                 </button>` 
              : '';

            return `
              <div class="comment-item reply-item" id="comment-${r.id}">
                <img class="comment-user-avatar" src="${r.avatar}" alt="${r.nickname}">
                <div class="comment-body">
                  <div class="comment-meta">
                    <span class="comment-nickname">${r.nickname}</span>
                    ${rRoleTag}
                    <span class="comment-time">${formatDate(r.createdAt)}</span>
                  </div>
                  <div class="comment-content">${escapeHTML(r.content)}</div>
                  <div class="comment-actions">
                    ${rDeleteBtn}
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    return `
      <div class="comment-item-group" data-id="${comment.id}">
        <div class="comment-item" id="comment-${comment.id}">
          <img class="comment-user-avatar" src="${comment.avatar}" alt="${comment.nickname}">
          <div class="comment-body">
            <div class="comment-meta">
              <span class="comment-nickname">${comment.nickname}</span>
              ${roleTag}
              <span class="comment-time">${formatDate(comment.createdAt)}</span>
            </div>
            <div class="comment-content">${escapeHTML(comment.content)}</div>
            <div class="comment-actions">
              ${replyBtn}
              ${deleteBtn}
            </div>
            
            <!-- Reply input container (Appended dynamically when clicked) -->
            <div class="reply-input-box" id="reply-container-${comment.id}" style="display: none;"></div>
          </div>
        </div>
        ${repliesHTML}
      </div>
    `;
  };

  /* --- 3. RENDER PROFILE PAGE --- */
  const renderUserProfile = (userId) => {
    const user = DB.auth.getCurrentUser();
    if (!user) return `<div class="empty-notif">프로필을 보려면 로그인해 주세요.</div>`;

    const commentsCount = DB.comments.getUserCommentsCount(user.id);
    const userLikes = DB.likes.getUserLikes(user.id);
    const userComments = DB.comments.getUserComments(user.id);

    const profile = document.createElement('div');
    profile.className = 'profile-page-wrapper';
    
    // Check if role is admin
    const adminTag = user.role === 'admin' ? '관리자 계정' : '일반 회원';

    profile.innerHTML = `
      <!-- User Profile Header Summary -->
      <div class="profile-header-card glass">
        <img class="profile-main-avatar" src="${user.avatar}" alt="${user.nickname}">
        <div class="profile-meta-info">
          <h2>${user.nickname} <span class="profile-stat-lbl">(@${user.username})</span></h2>
          <span class="profile-role-badge">${adminTag}</span>
          
          <div class="profile-stats-container">
            <div class="profile-stat-box">
              <div class="profile-stat-val">${userLikes.length}</div>
              <div class="profile-stat-lbl">좋아요 한 곡</div>
            </div>
            <div class="profile-stat-box">
              <div class="profile-stat-val">${commentsCount}</div>
              <div class="profile-stat-lbl">작성한 댓글</div>
            </div>
            <div class="profile-stat-box">
              <div class="profile-stat-val">${formatDate(user.createdAt, true)}</div>
              <div class="profile-stat-lbl">가입일</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detail Activity Tabs -->
      <div class="profile-tabs">
        <button class="profile-tab-btn active" data-tab="profile-likes">내가 좋아요 한 음악</button>
        <button class="profile-tab-btn" data-tab="profile-comments">내가 남긴 댓글</button>
      </div>

      <!-- Tab Contents -->
      <div class="profile-tab-content active" id="profile-likes">
        ${userLikes.length === 0 
          ? `<div class="empty-notif glass" style="padding: 4rem 0;">아직 좋아요 표시한 노래가 없습니다.</div>` 
          : `<div class="tracks-grid" id="profile-likes-grid"></div>`
        }
      </div>

      <div class="profile-tab-content" id="profile-comments">
        ${userComments.length === 0 
          ? `<div class="empty-notif glass" style="padding: 4rem 0;">작성한 댓글이 없습니다.</div>` 
          : `<div class="my-comments-list">
              ${userComments.map(c => `
                <div class="my-comment-item" data-music-id="${c.musicId}">
                  <div class="my-comment-left">
                    <div class="my-comment-music-title">
                      ${c.musicTitle}
                    </div>
                    <div class="my-comment-text">${escapeHTML(c.content)}</div>
                    <div class="my-comment-date">${formatDate(c.createdAt)}</div>
                  </div>
                  <div class="my-comment-link-icon">
                    ${getIcon('externalLink')}
                  </div>
                </div>
              `).join('')}
             </div>`
        }
      </div>
    `;

    // Inject cards into likes grid if any exist
    if (userLikes.length > 0) {
      setTimeout(() => {
        const grid = profile.querySelector('#profile-likes-grid');
        if (grid) {
          userLikes.forEach(like => {
            const songObj = YouTubeSearch.getCachedSong(like.musicId) || {
              id: like.musicId,
              title: like.musicTitle,
              channelTitle: 'MelodyLink Music',
              thumbnail: like.musicThumbnail,
              defaultTags: []
            };
            const card = renderMusicCard(songObj);
            grid.appendChild(card);
          });
        }
      }, 0);
    }

    return profile;
  };

  /* --- 4. RENDER ADMIN CONTROL PANEL --- */
  const renderAdminPanel = () => {
    const user = DB.auth.getCurrentUser();
    if (!user || user.role !== 'admin') {
      return `<div class="empty-notif glass">이 페이지에 접근할 권한이 없습니다.</div>`;
    }

    const users = DB.admin.getAllUsers();
    const comments = DB.admin.getAllComments();

    const panel = document.createElement('div');
    panel.className = 'admin-page-wrapper';

    panel.innerHTML = `
      <div class="admin-header">
        <h1>관리자 백오피스</h1>
        <p class="results-count">사용자 계정 상태와 댓글 데이터를 전역 관리합니다.</p>
      </div>

      <div class="admin-grid">
        <!-- User Management Card -->
        <div class="admin-section-card glass">
          <h2>회원 상태 관리 (${users.length}명)</h2>
          <div class="admin-table-wrapper">
            <table class="admin-table">
              <thead>
                <tr>
                  <th>아이디</th>
                  <th>닉네임</th>
                  <th>회원 등급</th>
                  <th>상태</th>
                  <th>계정 상태 변경</th>
                </tr>
              </thead>
              <tbody>
                ${users.map(u => {
                  const statusClass = u.isBlocked ? 'status-badge blocked' : 'status-badge active';
                  const statusText = u.isBlocked ? '이용 정지됨' : '활동 중';
                  const blockBtnText = u.isBlocked ? '정지 해제' : '활동 정지';
                  const isSelf = u.id === user.id;
                  
                  return `
                    <tr>
                      <td>
                        <img class="user-avatar-small" src="${u.avatar}" alt="avatar">
                        <strong>${u.username}</strong>
                      </td>
                      <td>${u.nickname}</td>
                      <td>
                        <span class="status-badge ${u.role === 'admin' ? 'active' : 'secondary'}">
                          ${u.role === 'admin' ? '관리자' : '일반회원'}
                        </span>
                        ${!isSelf && u.username !== 'admin' ? `
                          <button class="text-link-btn admin-role-toggle" data-user-id="${u.id}" style="margin-left: 0.5rem; font-size: 0.75rem;">
                            등급변경
                          </button>
                        ` : ''}
                      </td>
                      <td>
                        <span class="${statusClass}">${statusText}</span>
                      </td>
                      <td>
                        ${isSelf || u.username === 'admin'
                          ? `<span class="text-muted" style="font-size:0.8rem;">작업 불가 (본인)</span>`
                          : `<button class="btn btn-secondary btn-sm admin-block-toggle" data-user-id="${u.id}">
                              ${blockBtnText}
                             </button>`
                        }
                      </td>
                    </tr>
                  `;
                }).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Comments Management Card -->
        <div class="admin-section-card glass">
          <h2>전체 소셜 댓글 관리 (${comments.length}개)</h2>
          <div class="admin-table-wrapper">
            <table class="admin-table">
              <thead>
                <tr>
                  <th>곡 정보</th>
                  <th>작성자</th>
                  <th>내용</th>
                  <th>작성일</th>
                  <th>작업</th>
                </tr>
              </thead>
              <tbody>
                ${comments.map(c => `
                  <tr>
                    <td style="max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                      <a href="#music?id=${c.musicId}" class="text-link-btn" style="font-size: 0.85rem;">
                        ${c.musicTitle}
                      </a>
                    </td>
                    <td>
                      <span class="comment-nickname">${c.nickname}</span>
                    </td>
                    <td style="max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                      ${escapeHTML(c.content)}
                    </td>
                    <td class="comment-time">${formatDate(c.createdAt)}</td>
                    <td>
                      <button class="btn btn-danger btn-sm admin-delete-comment" data-comment-id="${c.id}">
                        삭제
                      </button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    return panel;
  };

  /* --- 5. RENDER TOAST NOTIFICATION CONTAINER --- */
  const renderNotificationToast = (notification) => {
    const toast = document.createElement('div');
    toast.className = 'toast info';
    toast.setAttribute('data-id', notification.id);
    
    toast.innerHTML = `
      <div class="toast-body">
        <div class="toast-title">${notification.senderNickname}님의 소통 알림</div>
        <div class="toast-text">${notification.content}</div>
        <div class="toast-text" style="font-size:0.7rem; color:var(--text-muted); margin-top:0.25rem;">
          곡: ${notification.musicTitle}
        </div>
      </div>
      <button class="toast-close" aria-label="닫기">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
      </button>
    `;

    return toast;
  };

  /* --- UTILITY: DATE FORMATTER --- */
  const formatDate = (isoString, dateOnly = false) => {
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return '';
    
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const date = String(d.getDate()).padStart(2, '0');
    
    if (dateOnly) {
      return `${year}-${month}-${date}`;
    }

    const hour = String(d.getHours()).padStart(2, '0');
    const min = String(d.getMinutes()).padStart(2, '0');

    // Return human-friendly elapsed time vs hard date
    const elapsedMs = Date.now() - d.getTime();
    const elapsedMin = Math.floor(elapsedMs / 60000);
    
    if (elapsedMin < 1) return '방금 전';
    if (elapsedMin < 60) return `${elapsedMin}분 전`;
    
    const elapsedHour = Math.floor(elapsedMin / 60);
    if (elapsedHour < 24) return `${elapsedHour}시간 전`;

    return `${year}.${month}.${date} ${hour}:${min}`;
  };

  /* --- UTILITY: XSS ESCAPER --- */
  const escapeHTML = (str) => {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  return {
    renderMusicCard,
    renderCommentSection,
    renderUserProfile,
    renderAdminPanel,
    renderNotificationToast,
    getIcon,
    formatDate,
    escapeHTML
  };
})();
