/* ----------------------------------------------------
   MelodyLink - YouTube API & Hybrid Search (youtube.js)
   Integrates YouTube API, Invidious Proxy, and Curated Local Library.
------------------------------------------------------- */

const YouTubeSearch = (() => {
  // Rich local curated library of actual real songs with active YouTube Video IDs
  const LOCAL_SONG_LIBRARY = [
    {
      id: 'pSUydWEqKwE',
      title: 'NewJeans (뉴진스) \'Ditto\' Official MV (Side A)',
      description: 'NewJeans (뉴진스) \'Ditto\' Official Music Video (Side A)\nStream Ditto on Spotify, Apple Music, YouTube Music. Produced by ADOR. Starring Minji, Hanni, Danielle, Haerin, Hyein. Winter sentiment track.',
      channelTitle: 'HYBE LABELS',
      thumbnail: 'https://i.ytimg.com/vi/pSUydWEqKwE/mqdefault.jpg',
      defaultTags: ['뉴진스', 'Ditto', '디토', '겨울감성', 'Ador', '신인']
    },
    {
      id: 'gdZLi9oWNzg',
      title: 'BTS (방탄소년단) \'Dynamite\' Official MV',
      description: 'BTS (방탄소년단) \'Dynamite\' Official MV\nDynamite is a disco-pop single that delivers joy, energy, and hope. Vocalists RM, Jin, SUGA, j-hope, Jimin, V, Jung Kook. Billboard Hot 100 #1 Hit.',
      channelTitle: 'HYBE LABELS',
      thumbnail: 'https://i.ytimg.com/vi/gdZLi9oWNzg/mqdefault.jpg',
      defaultTags: ['방탄소년단', 'BTS', 'Dynamite', '디스코팝', '신나는노래', '빌보드']
    },
    {
      id: 'v7bnOxyd4LI',
      title: 'IU (아이유) \'Love wins all\' MV',
      description: 'IU (아이유) \'Love wins all\' Official Music Video\nPre-release single from IU. Featuring V of BTS. A beautiful ballad conveying deep affection and perseverance. Directed by Um Tae-hwa.',
      channelTitle: '이지금 [IU Official]',
      thumbnail: 'https://i.ytimg.com/vi/v7bnOxyd4LI/mqdefault.jpg',
      defaultTags: ['아이유', 'IU', 'LoveWinsAll', '발라드', '감동', '뷔']
    },
    {
      id: 'ekr2nI1GP78',
      title: 'ROSÉ & Bruno Mars - APT. (Official Music Video)',
      description: 'ROSÉ & Bruno Mars - APT. (Official Music Video)\nStream APT. everywhere now. The global smash hit inspired by the Korean drinking game Apateu. High energy pop rock punk.',
      channelTitle: 'ROSÉ Official',
      thumbnail: 'https://i.ytimg.com/vi/ekr2nI1GP78/mqdefault.jpg',
      defaultTags: ['로제', '브루노마스', 'Rose', 'BrunoMars', '아파트', 'APT', '신나는노래']
    },
    {
      id: 'fJ9rUzIMcZQ',
      title: 'Queen – Bohemian Rhapsody (Official Video Improved)',
      description: 'Queen – Bohemian Rhapsody (Official Music Video)\nRecorded in 1975, Bohemian Rhapsody is a suite-like masterpiece containing opera, ballad, and hard rock sections. Legendary Freddie Mercury vocal performance.',
      channelTitle: 'Queen Official',
      thumbnail: 'https://i.ytimg.com/vi/fJ9rUzIMcZQ/mqdefault.jpg',
      defaultTags: ['Queen', 'BohemianRhapsody', '락', '클래식락', '퀸', '프레디머큐리']
    },
    {
      id: '11cta61wi0g',
      title: 'NewJeans (뉴진스) \'Hype Boy\' Official MV (Performance ver.1)',
      description: 'NewJeans (뉴진스) \'Hype Boy\' Official MV (Performance ver.1)\nStream Hype Boy now. Easy listening pop R&B track with unique choreography. ADOR Min Hee-jin production.',
      channelTitle: 'HYBE LABELS',
      thumbnail: 'https://i.ytimg.com/vi/11cta61wi0g/mqdefault.jpg',
      defaultTags: ['뉴진스', 'HypeBoy', '하입보이', '알앤비', '하이틴', '댄스']
    },
    {
      id: 'WMweEpGlu_U',
      title: 'BTS (방탄소년단) \'Butter\' Official MV',
      description: 'BTS (방탄소년단) \'Butter\' Official MV\nButter is a dance-pop track dripping with BTS charm. Smooth like butter, breaking dance moves, summery synth melodies.',
      channelTitle: 'HYBE LABELS',
      thumbnail: 'https://i.ytimg.com/vi/WMweEpGlu_U/mqdefault.jpg',
      defaultTags: ['방탄소년단', 'BTS', 'Butter', '댄스팝', '버터', '여름노래']
    },
    {
      id: 'v7GpFnYmI94',
      title: 'IU (아이유) \'LILAC\' (라일락) MV',
      description: 'IU (아이유) \'LILAC\' (라일락) Music Video\nTitle track of IU\'s 5th Album LILAC. Reflecting on her 20s and stepping into her 30s. Bright retro 70s-80s sound.',
      channelTitle: '이지금 [IU Official]',
      thumbnail: 'https://i.ytimg.com/vi/v7GpFnYmI94/mqdefault.jpg',
      defaultTags: ['아이유', 'IU', '라일락', 'LILAC', '시티팝', '댄스']
    },
    {
      id: 'IHNzAkXh9ys',
      title: 'BLACKPINK - \'뚜두뚜두 (DDU-DU DDU-DU)\' M/V',
      description: 'BLACKPINK - \'뚜두뚜두 (DDU-DU DDU-DU)\' Music Video\nProduced by TEDDY. Intense hip hop track with signature gun choreo. Global record breaker by Jisoo, Jennie, Rosé, Lisa.',
      channelTitle: 'BLACKPINK',
      thumbnail: 'https://i.ytimg.com/vi/IHNzAkXh9ys/mqdefault.jpg',
      defaultTags: ['블랙핑크', 'BLACKPINK', '뚜두뚜두', '힙합', '걸크러시', 'YG']
    },
    {
      id: 'OPf0YbXqDm0',
      title: 'Mark Ronson - Uptown Funk (Official Video) ft. Bruno Mars',
      description: 'Mark Ronson - Uptown Funk ft. Bruno Mars (Official Music Video)\nMulti-billion viewed retro funk track. Amazing horn section, groovy bassline, energetic vocals.',
      channelTitle: 'MarkRonsonVEVO',
      thumbnail: 'https://i.ytimg.com/vi/OPf0YbXqDm0/mqdefault.jpg',
      defaultTags: ['브루노마스', '마크론슨', 'UptownFunk', '펑크', '레트로', '댄스']
    },
    {
      id: 'dvgZkm1xWPE',
      title: 'Coldplay - Viva La Vida (Official Video)',
      description: 'Coldplay - Viva La Vida (Official Music Video)\nEpic orchestral alternative rock anthem. Baroque pop hooks, historical themes, violin section driven melody.',
      channelTitle: 'Coldplay',
      thumbnail: 'https://i.ytimg.com/vi/dvgZkm1xWPE/mqdefault.jpg',
      defaultTags: ['콜드플레이', 'Coldplay', 'VivaLaVida', '얼터너티브락', '밴드', '명곡']
    },
    {
      id: 'eVTXPUF4Oz4',
      title: 'In The End (Official Music Video) - Linkin Park',
      description: 'In The End (Official Video) by Linkin Park\nAlternative metal/rap rock masterpiece. Chester Bennington powerful vocals and Mike Shinoda rap delivery. Hybrid Theory.',
      channelTitle: 'Linkin Park',
      thumbnail: 'https://i.ytimg.com/vi/eVTXPUF4Oz4/mqdefault.jpg',
      defaultTags: ['린킨파크', 'LinkinPark', 'InTheEnd', '뉴메탈', '락', '명곡']
    }
  ];

  // Helper: Cache a searched song metadata into DB so detail views/likes can reference full details later
  const cacheSongDetails = (song) => {
    const cached = JSON.parse(localStorage.getItem('melodylink_cached_songs') || '{}');
    cached[song.id] = song;
    localStorage.setItem('melodylink_cached_songs', JSON.stringify(cached));
  };

  const getCachedSong = (id) => {
    const cached = JSON.parse(localStorage.getItem('melodylink_cached_songs') || '{}');
    // Check search library first
    const libraryMatch = LOCAL_SONG_LIBRARY.find(s => s.id === id);
    if (libraryMatch) return libraryMatch;
    
    return cached[id] || null;
  };

  /* --- SEARCH EXECUTOR (HYBRID) --- */
  const search = async (query = '') => {
    const settings = DB.settings.getSettings();
    const normalizedQuery = query.trim().toLowerCase();
    
    let apiResults = [];
    let isApiSuccess = false;

    // 1. If Query contains a hashtag sign (e.g. '#뉴진스'), normalize it
    const isExplicitTagSearch = normalizedQuery.startsWith('#');
    const cleanTagQuery = isExplicitTagSearch ? normalizedQuery.substring(1) : normalizedQuery;

    // 2. Try fetching from YouTube Official API or Invidious Proxy
    if (normalizedQuery.length > 0) {
      try {
        if (settings.apiKey) {
          apiResults = await fetchYouTubeOfficial(normalizedQuery, settings.apiKey);
          isApiSuccess = true;
        } else {
          apiResults = await fetchInvidious(normalizedQuery, settings.invidiousNode);
          isApiSuccess = true;
        }
      } catch (err) {
        console.warn('API Search failed or CORS issue, falling back to local query engine:', err);
      }
    }

    // 3. Cache API results metadata
    apiResults.forEach(track => cacheSongDetails(track));

    // 4. Local Database Hashtags Search
    // Get all songs that have a matching hashtag in LocalStorage (added by users)
    const localHashtags = JSON.parse(localStorage.getItem('melodylink_hashtags') || '[]');
    let hashtagMatchedMusicIds = [];

    if (normalizedQuery.length > 0) {
      hashtagMatchedMusicIds = localHashtags
        .filter(h => {
          const isMatch = isExplicitTagSearch 
            ? h.tag.toLowerCase() === cleanTagQuery 
            : h.tag.toLowerCase().includes(cleanTagQuery);
          return isMatch;
        })
        .map(h => h.musicId);
    }

    // 5. Gather and filter Local Library songs
    const localLibraryMatches = LOCAL_SONG_LIBRARY.filter(song => {
      if (normalizedQuery.length === 0) return true; // Show all by default

      // Title match
      const titleMatch = song.title.toLowerCase().includes(normalizedQuery);
      
      // Description match
      const descMatch = song.description.toLowerCase().includes(normalizedQuery);
      
      // Default tag match
      const defaultTagMatch = song.defaultTags.some(t => {
        return isExplicitTagSearch 
          ? t.toLowerCase() === cleanTagQuery 
          : t.toLowerCase().includes(cleanTagQuery);
      });

      // User added tag match
      const userTagMatch = hashtagMatchedMusicIds.includes(song.id);

      return titleMatch || descMatch || defaultTagMatch || userTagMatch;
    });

    // 6. Gather dynamically cached songs that match user hashtags but aren't in the local library
    const cachedSongs = JSON.parse(localStorage.getItem('melodylink_cached_songs') || '{}');
    const hashtagCachedMatches = [];
    
    hashtagMatchedMusicIds.forEach(id => {
      // If not already in library and exists in cached list
      if (!LOCAL_SONG_LIBRARY.some(s => s.id === id) && cachedSongs[id]) {
        hashtagCachedMatches.push(cachedSongs[id]);
      }
    });

    // 7. Merge and Deduplicate Results (API Results + Local Matches + Hashtag Cached Matches)
    const combined = [...apiResults];

    // Add local matches if they aren't already fetched from API
    localLibraryMatches.forEach(song => {
      if (!combined.some(s => s.id === song.id)) {
        combined.push(song);
      }
    });

    // Add hashtag matches from cached songs
    hashtagCachedMatches.forEach(song => {
      if (!combined.some(s => s.id === song.id)) {
        combined.push(song);
      }
    });

    // 8. If the search query was blank, return the entire local library (to make home page look populated)
    if (normalizedQuery.length === 0) {
      return LOCAL_SONG_LIBRARY;
    }

    return combined;
  };

  /* --- API FETCH WRAPPERS --- */

  // A. Invidious API (No key required, CORS-free on public servers)
  const fetchInvidious = async (query, instanceUrl) => {
    // URL-encode query
    const url = `${instanceUrl}/api/v1/search?q=${encodeURIComponent(query)}&type=video`;
    
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Invidious server returned status ${response.status}`);
    
    const data = await response.json();
    
    // Parse Invidious array to standard format
    // Format: Array of video items
    return data
      .filter(item => item.type === 'video')
      .slice(0, 15) // Limit to 15 results
      .map(item => ({
        id: item.videoId,
        title: item.title,
        description: item.description || '',
        channelTitle: item.author,
        thumbnail: (item.videoThumbnails && item.videoThumbnails.find(t => t.quality === 'medium' || t.quality === 'mqdefault')?.url) 
                   || `https://i.ytimg.com/vi/${item.videoId}/mqdefault.jpg`,
        defaultTags: []
      }));
  };

  // B. Official YouTube API v3 (Direct)
  const fetchYouTubeOfficial = async (query, apiKey) => {
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=15&q=${encodeURIComponent(query)}&key=${apiKey}`;
    
    const response = await fetch(url);
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(`YouTube API returned error: ${errData.error?.message || response.statusText}`);
    }
    
    const data = await response.json();
    
    return data.items.map(item => ({
      id: item.id.videoId,
      title: item.snippet.title,
      description: item.snippet.description,
      channelTitle: item.snippet.channelTitle,
      thumbnail: item.snippet.thumbnails?.medium?.url || `https://i.ytimg.com/vi/${item.id.videoId}/mqdefault.jpg`,
      defaultTags: []
    }));
  };

  return {
    search,
    getCachedSong,
    LOCAL_SONG_LIBRARY
  };
})();
