// components/Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:8050/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      
      if (response.ok) {
        setMessage('註冊成功，現在可以登入');
        navigate('/login');  // 註冊成功後跳轉到登入頁面
      } else {
        const data = await response.json();
        setMessage(data.error || '註冊失敗');
      }
    } catch (error) {
      setMessage('註冊失敗，請重試');
    }
  };

  return (
    <div>
      <h2>註冊</h2>
      <input placeholder="用戶名" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="密碼" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleRegister}>註冊</button>
      <p>{message}</p>
    </div>
  );
}

export default Register;
