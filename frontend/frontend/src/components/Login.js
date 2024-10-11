// src/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:8050/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessage(`註冊成功，歡迎 ${data.username}`);
      } else if (response.status === 409) {
        setMessage('用戶名已存在，請選擇其他用戶名');
        setUsername(''); // 清空用戶名輸入框
      } else {
        const errorData = await response.json();
        setMessage(`註冊失敗：${errorData.error}`);
      } 
    } catch (error) {
      console.error('Error in handleRegister:', error);
      setMessage('註冊失敗');
    }
  };

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:8050/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(`歡迎回來，${data.user.username}`);
        localStorage.setItem('username', data.user.username); // 儲存用戶名
        navigate('/Match'); // 跳轉到配對頁面
      } else {
        setMessage('登入失敗');
      }
    } catch (error) {
      console.error('Error in handleLogin:', error);
      setMessage('登入失敗');
    }
  };

  return (
    <div>
      <h2>註冊 / 登入</h2>
      <input placeholder="用戶名" value={username} onChange={e => setUsername(e.target.value)} />
      <input placeholder="密碼" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleRegister}>註冊</button>
      <button onClick={handleLogin}>登入</button>
      <p>{message}</p>
    </div>
  );
}

export default Login;
