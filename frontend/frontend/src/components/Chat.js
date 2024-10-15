import React, { useState, useEffect, useRef } from 'react'; 
import { useParams, useNavigate, useLocation } from 'react-router-dom';

function Chat() {
  const { matchId } = useParams();
  const [matchedUser, setMatchedUser] = useState('');
  const [message, setMessage] = useState('');
  const username = sessionStorage.getItem('username');
  const navigate = useNavigate();
  const location = useLocation();
  const heartbeatIntervalRef = useRef(null); // 用於心跳請求

  useEffect(() => {
    console.log(`[DEBUG] Username: ${username}`); // Debugging 用户名
    console.log(`[DEBUG] Match ID: ${matchId}`); // Debugging Match ID
    console.log(`[DEBUG] Location State:`, location.state); // Debugging 位置状态

    // 在位置狀態中獲取配對用戶
    if (location.state && location.state.matchedUsername) {
      console.log(`[DEBUG] 从 Location State 中获取的配对用户: ${location.state.matchedUsername}`);
      setMatchedUser(location.state.matchedUsername);
    } else {
      // 從後端獲取配對用戶
      const fetchMatchedUser = async () => {
        console.log(`[DEBUG] 正在从后端获取配对用户：${matchId}`);
        try {
          const response = await fetch(`http://localhost:8050/api/get-matched-user/${matchId}/?username=${username}`);
          const data = await response.json();
          if (response.ok) {
            console.log('[DEBUG] 成功获取配对用户:', data.matched_username);
            setMatchedUser(data.matched_username);
          } else {
            console.error('[ERROR] 获取配对对象失败:', data);
            setMessage('獲取配對對象失敗');
          }
        } catch (error) {
          console.error('[ERROR] 发生错误:', error);
          setMessage('獲取配對對象失敗');
        }
      };

      fetchMatchedUser();
    }

    // 發送心跳請求的函數
    const sendHeartbeat = () => {
      fetch('http://localhost:8050/api/heartbeat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
      })
      .then(response => response.json())
      .then(data => console.log('心跳已發送:', data.message))
      .catch(error => console.error('心跳錯誤:', error));
    };

    // 每30秒發送一次心跳請求
    heartbeatIntervalRef.current = setInterval(sendHeartbeat, 30000);
    
    return () => {
      // 組件卸載時清除定時器
      if (heartbeatIntervalRef.current) {
        clearInterval(heartbeatIntervalRef.current); // 清除心跳請求定時器
      }
    };
  }, [matchId, username, navigate, location.state]);

  const handleLike = async () => {
    console.log('[INFO] 用户点击了喜欢');
    try {
      const response = await fetch('http://localhost:8050/api/like/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          match_id: matchId,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        
      } else {
        alert('發送喜歡失敗');
        console.error('[ERROR] 發送喜歡失敗:', data);
      }
    } catch (error) {
      console.error('[ERROR] 發送喜歡請求出錯:', error);
    }
  };

  const handleLeave = () => {
    console.log('[INFO] 用户离开聊天页面');
    navigate('/Match'); // 返回配对页面
  };

  return (
    <div>
      <h2>聊天页面</h2>
      <p>配对对象：{matchedUser}</p>
      <div style={{ border: '1px solid black', height: '300px', overflowY: 'scroll' }}>
        {/* 這裡可以顯示聊天消息 */}
      </div>
      <input
        type="text"
        placeholder="输入消息"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={handleLike}>喜欢</button>
      <button onClick={handleLeave}>离开</button>
      <p>{message}</p>
    </div>
  );
}

export default Chat;
