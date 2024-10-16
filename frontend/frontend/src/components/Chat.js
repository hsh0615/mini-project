import React, { useState, useEffect, useRef } from 'react'; 
import { useParams, useNavigate, useLocation } from 'react-router-dom';

function Chat() {
  const { matchId } = useParams();
  const [matchedUser, setMatchedUser] = useState('');
  const [message, setMessage] = useState('');
  const [chatLog, setChatLog] = useState([]); // 儲存聊天記錄
  const [isConnected, setIsConnected] = useState(false); // 用於追踪 WebSocket 連接狀態
  const username = sessionStorage.getItem('username');
  const navigate = useNavigate();
  const location = useLocation();
  const heartbeatIntervalRef = useRef(null); // 用於心跳請求
  const socketRef = useRef(null); // WebSocket 引用

  useEffect(() => {
    console.log(`[DEBUG] Location State:`, location.state); // 打印状态以进行调试
    console.log(`[DEBUG] Username: ${username}`);
    console.log(`[DEBUG] Match ID: ${matchId}`);
    console.log(`[DEBUG] Location State:`, location.state);

    if (location.state && location.state.matchedUsername) {
      console.log(`[DEBUG] 从 Location State 中获取的配对用户: ${location.state.matchedUsername}`);
      setMatchedUser(location.state.matchedUsername);
    } else {
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

    heartbeatIntervalRef.current = setInterval(sendHeartbeat, 30000);
    
    return () => {
      if (heartbeatIntervalRef.current) {
        clearInterval(heartbeatIntervalRef.current);
      }
    };
  }, [matchId, username, navigate, location.state]);

  // 新增的 WebSocket useEffect
  useEffect(() => {
    // 初始化 WebSocket 連接
    const ws = new WebSocket(`ws://localhost:8080/ws/Chat/${matchId}/`);

    ws.onopen = () => {
      console.log('WebSocket 連接已建立');
      setIsConnected(true); // 更新連接狀態
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const { message, username } = data; // 获取消息和用户名
    
      // 检查用户名是否存在
      const displayName = username || 'Unknown';
    
      setChatLog(prevChatLog => [...prevChatLog, `${displayName}: ${message}`]);
    };
    

    ws.onclose = () => {
      console.log('WebSocket 連接已關閉');
      setIsConnected(false); // 更新連接狀態
    };

    socketRef.current = ws; // 存儲 WebSocket 連接

    return () => {
      if (socketRef.current) {
        socketRef.current.close(); // 清理 WebSocket 連接
      }
    };
  }, [matchId]);

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

  const handleSendMessage = () => {
    if (socketRef.current && message.trim()) {
      const msg = { username, message }; // 确保包含用户名
      socketRef.current.send(JSON.stringify(msg));
      setMessage('');
    }
  };
  
  

  return (
    <div>
      <h2>聊天页面</h2>
      <p>配对对象：{matchedUser}</p>
      <div style={{ border: '1px solid black', height: '300px', overflowY: 'scroll' }}>
        {/* 顯示聊天記錄 */}
        {chatLog.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <input
        type="text"
        placeholder="输入消息"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={handleSendMessage} disabled={!isConnected}>发送</button> {/* 新增發送按鈕 */}
      <button onClick={handleLike}>喜欢</button>
      <button onClick={handleLeave}>离开</button>
    </div>
  );
}

export default Chat;
