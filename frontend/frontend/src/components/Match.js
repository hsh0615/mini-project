// src/Matching.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Matching() {
  const [message, setMessage] = useState('配對中...');
  const username = localStorage.getItem('username');
  const navigate = useNavigate();

  useEffect(() => {
    if (!username) {
      navigate('/'); // 如果沒有用戶名，返回登入頁面
      return;
    }

    const enterMatchingPool = async () => {
      try {
        await fetch('http://localhost:8050/api/match/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username })
        });
      } catch (error) {
        console.error('Error in enterMatchingPool:', error);
        setMessage('配對請求失敗');
        return;
      }

      const pollMatchResult = async () => {
        try {
          const response = await fetch(`http://localhost:8050/api/match-result/${username}/`);
          const data = await response.json();

          if (data.message.includes('配對成功')) {
            setMessage(data.message);
            const matchId = data.match_id;
            navigate(`/chat/${matchId}`);
          } else {
            setTimeout(pollMatchResult, 5000);
          }
        } catch (error) {
          console.error('Error in pollMatchResult:', error);
          setMessage('配對結果查詢失敗');
        }
      };

      pollMatchResult();
    };

    enterMatchingPool();
  }, [username, navigate]);

  return (
    <div>
      <h2>配對頁面</h2>
      <p>{message}</p>
      <button onClick={() => navigate('/')}>登出</button>
    </div>
  );
}

export default Matching;
