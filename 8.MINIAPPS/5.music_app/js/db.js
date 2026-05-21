/* ----------------------------------------------------
   MelodyLink - LocalStorage Database Engine (db.js)
   Simulates all backend DB operations and seeds initial data.
------------------------------------------------------- */

const DB = (() => {
  // Storage Keys
  const KEYS = {
    USERS: 'melodylink_users',
    COMMENTS: 'melodylink_comments',
    LIKES: 'melodylink_likes',
    HASHTAGS: 'melodylink_hashtags',
    NOTIFICATIONS: 'melodylink_notifications',
    CURRENT_USER: 'melodylink_current_user',
    SETTINGS: 'melodylink_settings'
  };

  // Helper: Read/Write from LocalStorage
  const read = (key, fallback = []) => {
    try {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : fallback;
    } catch (e) {
      console.error(`LocalStorage read error for key [${key}]:`, e);
      return fallback;
    }
  };

  const write = (key, data) => {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
      console.error(`LocalStorage write error for key [${key}]:`, e);
    }
  };

  // Initialize DB and Seed Data if empty
  const init = () => {
    // 1. Initial Users
    if (!localStorage.getItem(KEYS.USERS)) {
      const seedUsers = [
        {
          id: 'u_admin',
          username: 'admin',
          nickname: '최고관리자',
          password: 'admin', // Simple auth for local miniapp demo
          role: 'admin',
          avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=admin',
          isBlocked: false,
          createdAt: new Date(Date.now() - 30 * 24 * 3600 * 1000).toISOString()
        },
        {
          id: 'u_music_lover',
          username: 'music_lover',
          nickname: '멜로디조아',
          password: 'password',
          role: 'user',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=music_lover',
          isBlocked: false,
          createdAt: new Date(Date.now() - 15 * 24 * 3600 * 1000).toISOString()
        },
        {
          id: 'u_beat_maker',
          username: 'beat_maker',
          nickname: '비트마스터',
          password: 'password',
          role: 'user',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=beat_maker',
          isBlocked: false,
          createdAt: new Date(Date.now() - 10 * 24 * 3600 * 1000).toISOString()
        },
        {
          id: 'u_kpop_fan',
          username: 'kpop_fan',
          nickname: '케이팝덕후',
          password: 'password',
          role: 'user',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=kpop_fan',
          isBlocked: false,
          createdAt: new Date(Date.now() - 5 * 24 * 3600 * 1000).toISOString()
        }
      ];
      write(KEYS.USERS, seedUsers);
    }

    // 2. Initial Likes
    if (!localStorage.getItem(KEYS.LIKES)) {
      const seedLikes = [
        // music_lover likes Ditto
        { userId: 'u_music_lover', musicId: 'pSUydWEqKwE', musicTitle: 'NewJeans (뉴진스) \'Ditto\'', musicThumbnail: 'https://i.ytimg.com/vi/pSUydWEqKwE/mqdefault.jpg', createdAt: new Date(Date.now() - 2 * 24 * 3600 * 1000).toISOString() },
        // music_lover likes Dynamite
        { userId: 'u_music_lover', musicId: 'gdZLi9oWNzg', musicTitle: 'BTS (방탄소년단) \'Dynamite\'', musicThumbnail: 'https://i.ytimg.com/vi/gdZLi9oWNzg/mqdefault.jpg', createdAt: new Date(Date.now() - 1 * 24 * 3600 * 1000).toISOString() },
        // beat_maker likes Ditto
        { userId: 'u_beat_maker', musicId: 'pSUydWEqKwE', musicTitle: 'NewJeans (뉴진스) \'Ditto\'', musicThumbnail: 'https://i.ytimg.com/vi/pSUydWEqKwE/mqdefault.jpg', createdAt: new Date(Date.now() - 2 * 24 * 3600 * 1000).toISOString() },
        // kpop_fan likes Love wins all
        { userId: 'u_kpop_fan', musicId: 'v7bnOxyd4LI', musicTitle: 'IU (아이유) \'Love wins all\'', musicThumbnail: 'https://i.ytimg.com/vi/v7bnOxyd4LI/mqdefault.jpg', createdAt: new Date(Date.now() - 3 * 24 * 3600 * 1000).toISOString() }
      ];
      write(KEYS.LIKES, seedLikes);
    }

    // 3. Initial Comments
    if (!localStorage.getItem(KEYS.COMMENTS)) {
      const seedComments = [
        // Ditto comments
        {
          id: 'c1',
          musicId: 'pSUydWEqKwE',
          musicTitle: 'NewJeans (뉴진스) \'Ditto\'',
          userId: 'u_music_lover',
          username: 'music_lover',
          nickname: '멜로디조아',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=music_lover',
          content: '이 노래는 도입부 허밍 소리만 들어도 가슴이 몽글몽글해지네요. 겨울 감성 종결곡!',
          createdAt: new Date(Date.now() - 4 * 3600 * 1000).toISOString(),
          parentId: null
        },
        {
          id: 'c2',
          musicId: 'pSUydWEqKwE',
          musicTitle: 'NewJeans (뉴진스) \'Ditto\'',
          userId: 'u_beat_maker',
          username: 'beat_maker',
          nickname: '비트마스터',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=beat_maker',
          content: '진짜 동감합니다. 특히 비트 드럼 라인이 독특해서 들을 때마다 신선하네요.',
          createdAt: new Date(Date.now() - 3.5 * 3600 * 1000).toISOString(),
          parentId: 'c1' // Reply to c1
        },
        {
          id: 'c3',
          musicId: 'pSUydWEqKwE',
          musicTitle: 'NewJeans (뉴진스) \'Ditto\'',
          userId: 'u_kpop_fan',
          username: 'kpop_fan',
          nickname: '케이팝덕후',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=kpop_fan',
          content: '뮤직비디오 스토리라인 해석하면서 보면 감동이 100배가 됩니다 ㅠㅠ 반희수 최고!',
          createdAt: new Date(Date.now() - 2 * 3600 * 1000).toISOString(),
          parentId: null
        },
        // Dynamite comments
        {
          id: 'c4',
          musicId: 'gdZLi9oWNzg',
          musicTitle: 'BTS (방탄소년단) \'Dynamite\'',
          userId: 'u_kpop_fan',
          username: 'kpop_fan',
          nickname: '케이팝덕후',
          avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=kpop_fan',
          content: '들으면 항상 기분이 좋아지는 디스코 팝! 빌보드 1위 클래스 영원하길!',
          createdAt: new Date(Date.now() - 6 * 3600 * 1000).toISOString(),
          parentId: null
        }
      ];
      write(KEYS.COMMENTS, seedComments);
    }

    // 4. Initial Hashtags
    if (!localStorage.getItem(KEYS.HASHTAGS)) {
      const seedHashtags = [
        { musicId: 'pSUydWEqKwE', tag: '뉴진스', userId: 'u_music_lover', createdAt: new Date().toISOString() },
        { musicId: 'pSUydWEqKwE', tag: 'Ditto', userId: 'u_beat_maker', createdAt: new Date().toISOString() },
        { musicId: 'pSUydWEqKwE', tag: '겨울감성', userId: 'u_music_lover', createdAt: new Date().toISOString() },
        { musicId: 'gdZLi9oWNzg', tag: '방탄소년단', userId: 'u_kpop_fan', createdAt: new Date().toISOString() },
        { musicId: 'gdZLi9oWNzg', tag: '신나는노래', userId: 'u_music_lover', createdAt: new Date().toISOString() },
        { musicId: 'v7bnOxyd4LI', tag: '아이유', userId: 'u_kpop_fan', createdAt: new Date().toISOString() },
        { musicId: 'v7bnOxyd4LI', tag: '발라드', userId: 'u_kpop_fan', createdAt: new Date().toISOString() },
        { musicId: 'fJ9rUzIMcZQ', tag: 'Queen', userId: 'u_beat_maker', createdAt: new Date().toISOString() },
        { musicId: 'fJ9rUzIMcZQ', tag: '락', userId: 'u_beat_maker', createdAt: new Date().toISOString() }
      ];
      write(KEYS.HASHTAGS, seedHashtags);
    }

    // 5. Initial Notifications (To show users their alerts are working immediately)
    if (!localStorage.getItem(KEYS.NOTIFICATIONS)) {
      const seedNotifications = [
        {
          id: 'n1',
          userId: 'u_music_lover', // Recipient
          senderId: 'u_beat_maker',
          senderNickname: '비트마스터',
          type: 'comment',
          musicId: 'pSUydWEqKwE',
          musicTitle: 'NewJeans (뉴진스) \'Ditto\'',
          content: '진짜 동감합니다. 특히 비트 드럼 라인이...',
          isRead: false,
          createdAt: new Date(Date.now() - 3.5 * 3600 * 1000).toISOString()
        }
      ];
      write(KEYS.NOTIFICATIONS, seedNotifications);
    }

    // 6. Settings Default
    if (!localStorage.getItem(KEYS.SETTINGS)) {
      write(KEYS.SETTINGS, {
        apiKey: '',
        invidiousNode: 'https://invidious.private.coffee',
        browserPush: false
      });
    }
  };

  /* --- AUTH METHODS --- */
  const getCurrentUser = () => {
    return read(KEYS.CURRENT_USER, null);
  };

  const login = (username, password) => {
    const users = read(KEYS.USERS);
    const user = users.find(u => u.username.toLowerCase() === username.toLowerCase());
    
    if (!user) {
      return { success: false, message: '존재하지 않는 아이디입니다.' };
    }
    
    if (user.password !== password) {
      return { success: false, message: '비밀번호가 올바르지 않습니다.' };
    }

    if (user.isBlocked) {
      return { success: false, message: '이 계정은 관리자에 의해 이용 정지되었습니다.' };
    }

    // Write login session
    write(KEYS.CURRENT_USER, user);
    return { success: true, user };
  };

  const signup = (username, nickname, password) => {
    const users = read(KEYS.USERS);
    
    if (users.some(u => u.username.toLowerCase() === username.toLowerCase())) {
      return { success: false, message: '이미 가입된 아이디입니다.' };
    }
    if (users.some(u => u.nickname === nickname)) {
      return { success: false, message: '이미 사용 중인 닉네임입니다.' };
    }

    const newUser = {
      id: 'u_' + Math.random().toString(36).substr(2, 9),
      username,
      nickname,
      password,
      role: 'user',
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${nickname}`,
      isBlocked: false,
      createdAt: new Date().toISOString()
    };

    users.push(newUser);
    write(KEYS.USERS, users);
    
    // Auto login
    write(KEYS.CURRENT_USER, newUser);
    return { success: true, user: newUser };
  };

  const logout = () => {
    localStorage.removeItem(KEYS.CURRENT_USER);
    return true;
  };

  /* --- LIKES METHODS --- */
  const toggleLike = (musicId, musicTitle, musicThumbnail) => {
    const user = getCurrentUser();
    if (!user) return { success: false, error: 'login_required' };

    let likes = read(KEYS.LIKES);
    const existingIndex = likes.findIndex(l => l.userId === user.id && l.musicId === musicId);
    let liked = false;

    if (existingIndex > -1) {
      likes.splice(existingIndex, 1);
    } else {
      likes.push({
        userId: user.id,
        musicId,
        musicTitle,
        musicThumbnail,
        createdAt: new Date().toISOString()
      });
      liked = true;
    }

    write(KEYS.LIKES, likes);
    return { success: true, liked, likesCount: getLikesCount(musicId) };
  };

  const isLiked = (musicId) => {
    const user = getCurrentUser();
    if (!user) return false;
    const likes = read(KEYS.LIKES);
    return likes.some(l => l.userId === user.id && l.musicId === musicId);
  };

  const getLikesCount = (musicId) => {
    const likes = read(KEYS.LIKES);
    return likes.filter(l => l.musicId === musicId).length;
  };

  const getUserLikes = (userId) => {
    const likes = read(KEYS.LIKES);
    return likes.filter(l => l.userId === userId);
  };

  /* --- COMMENTS METHODS --- */
  const getComments = (musicId) => {
    const comments = read(KEYS.COMMENTS);
    return comments.filter(c => c.musicId === musicId).sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
  };

  const addComment = (musicId, musicTitle, content, parentId = null) => {
    const user = getCurrentUser();
    if (!user) return { success: false, error: 'login_required' };
    if (user.isBlocked) return { success: false, error: 'blocked' };

    const comments = read(KEYS.COMMENTS);
    const newComment = {
      id: 'c_' + Math.random().toString(36).substr(2, 9),
      musicId,
      musicTitle,
      userId: user.id,
      username: user.username,
      nickname: user.nickname,
      avatar: user.avatar,
      content,
      createdAt: new Date().toISOString(),
      parentId
    };

    comments.push(newComment);
    write(KEYS.COMMENTS, comments);

    // CRITICAL REQ: Send Push Notifications to other users who LIKED this music
    triggerCommentNotifications(newComment, musicTitle);

    return { success: true, comment: newComment };
  };

  // Find users who liked this music and notify them
  const triggerCommentNotifications = (comment, musicTitle) => {
    const likes = read(KEYS.LIKES);
    // Find unique user IDs who liked this track and are NOT the commentator
    const userIdsToNotify = [...new Set(
      likes
        .filter(l => l.musicId === comment.musicId && l.userId !== comment.userId)
        .map(l => l.userId)
    )];

    userIdsToNotify.forEach(recipientId => {
      addNotification(
        recipientId,
        comment.userId,
        comment.nickname,
        'comment',
        comment.musicId,
        musicTitle,
        comment.content
      );
    });
  };

  const deleteComment = (commentId) => {
    const user = getCurrentUser();
    if (!user) return { success: false, error: 'login_required' };

    let comments = read(KEYS.COMMENTS);
    const comment = comments.find(c => c.id === commentId);

    if (!comment) return { success: false, error: 'not_found' };

    // Auth check: Admin or the owner can delete
    if (user.role !== 'admin' && comment.userId !== user.id) {
      return { success: false, error: 'unauthorized' };
    }

    // Delete comment and its sub-replies recursively
    const commentsToDelete = [commentId];
    let search = true;
    while (search) {
      const childCount = commentsToDelete.length;
      comments.forEach(c => {
        if (c.parentId && commentsToDelete.includes(c.parentId) && !commentsToDelete.includes(c.id)) {
          commentsToDelete.push(c.id);
        }
      });
      if (commentsToDelete.length === childCount) {
        search = false;
      }
    }

    comments = comments.filter(c => !commentsToDelete.includes(c.id));
    write(KEYS.COMMENTS, comments);

    return { success: true, deletedIds: commentsToDelete };
  };

  /* --- HASHTAGS METHODS --- */
  const addHashtag = (musicId, tag) => {
    const user = getCurrentUser();
    if (!user) return { success: false, error: 'login_required' };

    // Normalize tag: strip out '#' symbol, trim whitespace
    const cleanTag = tag.replace(/#/g, '').trim();
    if (!cleanTag) return { success: false, error: 'invalid_tag' };

    let hashtags = read(KEYS.HASHTAGS);
    
    // Check if the hashtag is already added to this track
    const exists = hashtags.some(h => h.musicId === musicId && h.tag.toLowerCase() === cleanTag.toLowerCase());
    
    if (exists) {
      return { success: false, error: 'tag_exists' };
    }

    const newTag = {
      musicId,
      tag: cleanTag,
      userId: user.id,
      createdAt: new Date().toISOString()
    };

    hashtags.push(newTag);
    write(KEYS.HASHTAGS, hashtags);

    return { success: true, tag: newTag };
  };

  const getHashtags = (musicId) => {
    const hashtags = read(KEYS.HASHTAGS);
    return hashtags.filter(h => h.musicId === musicId);
  };

  const getAllHashtags = () => {
    const hashtags = read(KEYS.HASHTAGS);
    // Count frequencies
    const counts = {};
    hashtags.forEach(h => {
      const norm = h.tag.trim();
      counts[norm] = (counts[norm] || 0) + 1;
    });

    // Return sorted list of { tag, count }
    return Object.keys(counts)
      .map(tag => ({ tag, count: counts[tag] }))
      .sort((a, b) => b.count - a.count);
  };

  /* --- NOTIFICATIONS METHODS --- */
  const getNotifications = () => {
    const user = getCurrentUser();
    if (!user) return [];
    
    const notifications = read(KEYS.NOTIFICATIONS);
    return notifications
      .filter(n => n.userId === user.id)
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  };

  const addNotification = (userId, senderId, senderNickname, type, musicId, musicTitle, content) => {
    const notifications = read(KEYS.NOTIFICATIONS);
    const newNotif = {
      id: 'n_' + Math.random().toString(36).substr(2, 9),
      userId,
      senderId,
      senderNickname,
      type,
      musicId,
      musicTitle,
      content: content.length > 35 ? content.substr(0, 35) + '...' : content,
      isRead: false,
      createdAt: new Date().toISOString()
    };

    notifications.push(newNotif);
    write(KEYS.NOTIFICATIONS, notifications);

    // If the recipient user is currently online (logged in), dispatch a live DOM event for immediate toast display
    const currentUser = getCurrentUser();
    if (currentUser && currentUser.id === userId) {
      const event = new CustomEvent('melodylink_push_notification', { detail: newNotif });
      window.dispatchEvent(event);
    }

    // Trigger Browser Push if allowed and supported
    triggerBrowserPush(newNotif);

    return newNotif;
  };

  const markAsRead = (notificationId) => {
    const notifications = read(KEYS.NOTIFICATIONS);
    const index = notifications.findIndex(n => n.id === notificationId);
    if (index > -1) {
      notifications[index].isRead = true;
      write(KEYS.NOTIFICATIONS, notifications);
      return true;
    }
    return false;
  };

  const markAllAsRead = () => {
    const user = getCurrentUser();
    if (!user) return false;

    const notifications = read(KEYS.NOTIFICATIONS);
    notifications.forEach(n => {
      if (n.userId === user.id) {
        n.isRead = true;
      }
    });
    write(KEYS.NOTIFICATIONS, notifications);
    return true;
  };

  const triggerBrowserPush = (notif) => {
    const settings = getSettings();
    if (settings.browserPush && 'Notification' in window && Notification.permission === 'granted') {
      const bodyText = notif.type === 'comment' 
        ? `'${notif.musicTitle}' 음악에 ${notif.senderNickname}님이 댓글을 남겼습니다: ${notif.content}`
        : `${notif.senderNickname}님이 새로운 소식을 보냈습니다.`;
      
      new Notification('MelodyLink 알림', {
        body: bodyText,
        icon: 'https://img.icons8.com/color/96/musical-notes.png'
      });
    }
  };

  /* --- SYSTEM SETTINGS --- */
  const getSettings = () => {
    return read(KEYS.SETTINGS, { apiKey: '', invidiousNode: 'https://invidious.private.coffee', browserPush: false });
  };

  const saveSettings = (newSettings) => {
    write(KEYS.SETTINGS, newSettings);
    return true;
  };

  /* --- ADMIN PANEL METHODS --- */
  const getAllUsers = () => {
    const user = getCurrentUser();
    if (!user || user.role !== 'admin') return [];
    return read(KEYS.USERS);
  };

  const toggleBlockUser = (userId) => {
    const user = getCurrentUser();
    if (!user || user.role !== 'admin') return { success: false, error: 'unauthorized' };
    if (userId === 'u_admin') return { success: false, error: 'cannot_block_root_admin' };

    const users = read(KEYS.USERS);
    const index = users.findIndex(u => u.id === userId);
    
    if (index > -1) {
      users[index].isBlocked = !users[index].isBlocked;
      write(KEYS.USERS, users);
      
      // If blocked user is currently logged in, force session logout
      const currentLoggedIn = getCurrentUser();
      if (currentLoggedIn && currentLoggedIn.id === userId && users[index].isBlocked) {
        logout();
      }
      return { success: true, isBlocked: users[index].isBlocked };
    }
    return { success: false, error: 'not_found' };
  };

  const changeUserRole = (userId) => {
    const user = getCurrentUser();
    if (!user || user.role !== 'admin') return { success: false, error: 'unauthorized' };
    if (userId === 'u_admin') return { success: false, error: 'cannot_change_root_admin' };

    const users = read(KEYS.USERS);
    const index = users.findIndex(u => u.id === userId);
    
    if (index > -1) {
      users[index].role = users[index].role === 'admin' ? 'user' : 'admin';
      write(KEYS.USERS, users);
      return { success: true, role: users[index].role };
    }
    return { success: false, error: 'not_found' };
  };

  const getAllComments = () => {
    const user = getCurrentUser();
    if (!user || user.role !== 'admin') return [];
    return read(KEYS.COMMENTS).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  };

  const getUserCommentsCount = (userId) => {
    const comments = read(KEYS.COMMENTS);
    return comments.filter(c => c.userId === userId).length;
  };

  const getUserComments = (userId) => {
    const comments = read(KEYS.COMMENTS);
    return comments
      .filter(c => c.userId === userId)
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  };

  return {
    init,
    auth: {
      getCurrentUser,
      login,
      signup,
      logout
    },
    likes: {
      toggleLike,
      isLiked,
      getLikesCount,
      getUserLikes
    },
    comments: {
      getComments,
      addComment,
      deleteComment,
      getUserComments,
      getUserCommentsCount
    },
    hashtags: {
      addHashtag,
      getHashtags,
      getAllHashtags
    },
    notifications: {
      getNotifications,
      markAsRead,
      markAllAsRead
    },
    settings: {
      getSettings,
      saveSettings
    },
    admin: {
      getAllUsers,
      toggleBlockUser,
      changeUserRole,
      getAllComments
    }
  };
})();

// Auto-run DB init on import/execution
DB.init();
