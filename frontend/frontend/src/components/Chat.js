// src/Chat.js
import React, { useState, useEffect } from 'react'; 
import { useParams, useNavigate } from 'react-router-dom';

function Chat() {
  const { matchId } = useParams();
  const [matchedUser, setMatchedUser] = useState('');
  const [message, setMessage] = useState('');
  const username = localStorage.getItem('username');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMatchedUser = async () => {
      try {
        const response = await fetch(`http://localhost:8050/api/get-matched-user/${matchId}/?username=${username}`);
        const data = await response.json();
        if (response.ok) {
          setMatchedUser(data.matched_username);
        } else {
          setMessage('獲取配對對象失敗');
        }
      } catch (error) {
        console.error('Error fetching matched user:', error);
        setMessage('獲取配對對象失敗');
      }
    };

    fetchMatchedUser();
  }, [matchId, username]);

  const handleLike = async () => {
    // 實現「喜歡」的功能
  };

  const handleLeave = () => {
    navigate('/Match'); // 返回配對頁面
  };

  return (
    <div>
      <h2>聊天頁面</h2>
      <p>配對對象：{matchedUser}</p>
      {/* 這裡可以添加聊天訊息的顯示 */}
      <input type="text" placeholder="輸入訊息" />
      <button onClick={handleLike}>喜歡</button>
      <button onClick={handleLeave}>離開</button>
      <p>{message}</p>
    </div>
  );
}

export default Chat;
