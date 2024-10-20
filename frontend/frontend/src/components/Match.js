import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Box, CircularProgress } from '@mui/material'; // 引入 MUI 組件


function Match() {
  const [message, setMessage] = useState('');
  const [isMatching, setIsMatching] = useState(false);
  const username = sessionStorage.getItem('username');
  const navigate = useNavigate();
  const intervalRef = useRef(null);
  const heartbeatIntervalRef = useRef(null); // 用於心跳請求

  useEffect(() => {
    const sendHeartbeat = () => {
      fetch('http://localhost:8050/api/heartbeat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      })
        .then((response) => response.json())
        .then((data) => console.log('心跳已發送:', data.message))
        .catch((error) => console.error('心跳錯誤:', error));
    };

    // 在這裡立即發送心跳請求
    sendHeartbeat();
    
    heartbeatIntervalRef.current = setInterval(sendHeartbeat, 30000);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (heartbeatIntervalRef.current) clearInterval(heartbeatIntervalRef.current);
    };
  }, [username]);

  const handleMatch = async () => {
    setIsMatching(true);
    setMessage('等待配對中...');

    try {
      const response = await fetch('http://localhost:8050/api/match/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();
      if (response.ok && data.match_id) {
        navigate(`/Chat/${data.match_id}`, { state: { matchedUsername: data.matched_username } });
      } else {
        pollMatchResult(); // 輪詢配對結果
      }
    } catch (error) {
      console.error('配對請求失敗:', error);
      setMessage('配對請求失敗');
      setIsMatching(false);
    }
  };

  const pollMatchResult = () => {
    intervalRef.current = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:8050/api/match-result/${username}/`);
        const data = await response.json();

        if (data.match_id) {
          clearInterval(intervalRef.current);
          console.log('[DEBUG] Data before navigating:', data);
          navigate(`/Chat/${data.match_id}`, { state: { matchedUsername: data.matched_username } });
        } else {
          setMessage(data.message || '等待配對中...');
        }
      } catch (error) {
        console.error('輪詢配對結果失敗:', error);
      }
    }, 5000);
  };

  const handleCancelMatch = async () => {
    try {
      const response = await fetch('http://localhost:8050/api/cancel-match/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        setIsMatching(false);
        if (intervalRef.current) clearInterval(intervalRef.current);
      } else {
        setMessage(data.message || '取消配對失敗');
      }
    } catch (error) {
      console.error('取消配對請求失敗:', error);
      setMessage('取消配對請求失敗');
    }
  };

//   return (
//     <div>
//       <h1>配對頁面</h1>
//       <p>{message}</p>
//       {isMatching ? (
//         <>
//           <button onClick={handleCancelMatch}>取消配對</button>
//         </>
//       ) : (
//         <button onClick={handleMatch}>開始配對</button>
//       )}
//       <button onClick={() => navigate('/friends')}>好友列表</button>
//     </div>
//   );
// }

// export default Match;
return (
  <Box
    display="flex"
    flexDirection="column"
    alignItems="center"
    justifyContent="center"
    minHeight="100vh"
    padding={2}
  >
    <Typography variant="h4" gutterBottom>
      配對頁面
    </Typography>
    <Typography variant="body1" gutterBottom color="textSecondary">
      {message}
    </Typography>
    {isMatching ? (
      <>
        <Button
          variant="contained"
          color="error"
          onClick={handleCancelMatch}
          fullWidth
          sx={{ mt: 2, mb: 2 }}
        >
          取消配對
        </Button>
      </>
    ) : (
      <Button
        variant="contained"
        color="primary"
        onClick={handleMatch}
        fullWidth
        sx={{ mt: 2, mb: 2 }}
      >
        {isMatching ? <CircularProgress size={24} /> : '開始配對'}
      </Button>
    )}
    <Button
      variant="outlined"
      onClick={() => navigate('/friends')}
      fullWidth
      sx={{ mt: 2 }}
    >
      好友列表
    </Button>
  </Box>
);
}

export default Match;
