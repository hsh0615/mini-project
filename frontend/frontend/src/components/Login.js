// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Box, Typography, CircularProgress } from '@mui/material'; // 引入 MUI 組件

function Login() {
  const [username, setUsername] = useState(sessionStorage.getItem('username') || '');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false); // 用於顯示 loading 狀態
  const navigate = useNavigate();

  const handleRegister = async () => {
    setLoading(true); // 開始 loading
    try {
      const response = await fetch('http://localhost:8050/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`註冊成功，歡迎 ${data.data.username}！`);
      } else if (response.status === 409) {
        setMessage('用戶名已存在，請選擇其他用戶名');
        setUsername(''); // 清空用戶名輸入框
      } else {
        setMessage(`註冊失敗：${data.error.message}`);
      }
    } catch (error) {
      console.error('Error in handleRegister:', error);
      setMessage('註冊失敗，請稍後再試。');
    } finally {
      setLoading(false); // 結束 loading
    }
  };

  const handleLogin = async () => {
    setLoading(true); // 開始 loading
    try {
      const response = await fetch('http://localhost:8050/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`歡迎回來，${data.data.username}！`);
        sessionStorage.setItem('username', data.data.username); // 儲存用戶名
        navigate('/Match'); // 跳轉到配對頁面
      } else {
        setMessage(data.error ? data.error.message : '登入失敗');
      }
    } catch (error) {
      console.error('Error in handleLogin:', error);
      setMessage('登入失敗，請稍後再試。');
    } finally {
      setLoading(false); // 結束 loading
      setPassword(''); // 清空密碼輸入框
    }
  };

//   return (
//     <div>
//       <h2>註冊 / 登入</h2>
//       <input
//         placeholder="用戶名"
//         value={username}
//         onChange={e => setUsername(e.target.value)}
//       />
//       <input
//         placeholder="密碼"
//         type="password"
//         value={password}
//         onChange={e => setPassword(e.target.value)}
//       />
//       <button onClick={handleRegister} disabled={loading}>
//         {loading ? '註冊中...' : '註冊'}
//       </button>
//       <button onClick={handleLogin} disabled={loading}>
//         {loading ? '登入中...' : '登入'}
//       </button>
//       <p>{message}</p>
//     </div>
//   );
// }

// export default Login;
return (
  <Box
    display="flex"
    flexDirection="column"
    alignItems="center"
    justifyContent="center"
    minHeight="100vh"
    padding={2}
  >
    <Typography variant="h4" gutterBottom>註冊 / 登入</Typography>

    <TextField
      label="用戶名"
      variant="outlined"
      value={username}
      onChange={e => setUsername(e.target.value)}
      margin="normal"
      fullWidth
    />

    <TextField
      label="密碼"
      type="password"
      variant="outlined"
      value={password}
      onChange={e => setPassword(e.target.value)}
      margin="normal"
      fullWidth
    />

    <Box display="flex" justifyContent="space-between" width="100%" mt={2}>
      <Button
        variant="contained"
        color="primary"
        onClick={handleRegister}
        disabled={loading}
        fullWidth
        style={{ marginRight: '10px' }}
      >
        {loading ? <CircularProgress size={24} /> : '註冊'}
      </Button>

      <Button
        variant="contained"
        color="secondary"
        onClick={handleLogin}
        disabled={loading}
        fullWidth
      >
        {loading ? <CircularProgress size={24} /> : '登入'}
      </Button>
    </Box>

    {message && (
      <Typography color="error" variant="body1" mt={2}>
        {message}
      </Typography>
    )}
  </Box>
);
}

export default Login;
