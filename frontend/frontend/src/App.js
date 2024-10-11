// import React, { useState } from 'react';

// function App() {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [message, setMessage] = useState('');

//   const handleRegister = async () => {
//     try {
//       const response = await fetch('http://localhost:8050/api/register/', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ username, password })
//       });
      
//       if (response.ok) {
//         const data = await response.json();
//         setMessage(`Registered as ${data.username}`);
//       } else if (response.status === 409) {
//         setMessage('用戶名已存在，請選擇其他用戶名');
//         setUsername(''); // 清空用戶名輸入框
//       } else {
//         const errorData = await response.json();
//         setMessage(`註冊失敗：${errorData.error}`);
//       } 
//     } catch (error) {
//       console.error('Error in handleRegister:', error);
//       setMessage('註冊失敗');
//     }
//   };

//   const handleLogin = async () => {
//     try {
//       const response = await fetch('http://localhost:8050/api/login/', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ username, password })
//       });
//       const data = await response.json();
//       if (response.ok) {
//         setMessage(`Welcome back, ${data.user.username}`);
//       } else {
//         setMessage('Login failed');
//       }
//     } catch (error) {
//       console.error('Error in handleLogin:', error);
//       setMessage('Login failed');
//     }
//   };

//   const handleMatch = async () => {
//     setMessage('配對中...');

//     // 發送配對請求
//     try {
//       await fetch('http://localhost:8050/api/match', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ username })
//       });
//     } catch (error) {
//       console.error('Error in handleMatch:', error);
//       setMessage('配對請求失敗');
//       return;
//     }

//     // 輪詢配對結果
//     const pollMatchResult = async () => {
//       try {
//         const response = await fetch(`http://localhost:8050/api/match-result/${username}`);
//         const data = await response.json();

//         if (data.message.includes('配對成功')) {
//           setMessage(data.message); // 配對成功，顯示消息
//         } else {
//           setTimeout(pollMatchResult, 5000); // 還在等待，繼續輪詢
//         }
//       } catch (error) {
//         console.error('Error in pollMatchResult:', error);
//         setMessage('配對結果查詢失敗');
//       }
//     };

//     pollMatchResult(); // 發送第一次配對結果查詢請求
//   };

//   return (
//     <div>
//       <h2>Register / Login</h2>
//       <input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
//       <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
//       <button onClick={handleRegister}>Register</button>
//       <button onClick={handleLogin}>Login</button>
//       <button onClick={handleMatch}>配對</button>
//       <p>{message}</p>
//     </div>
//   );
// }

// export default App;

// src/App.js
import React from 'react'; 
//import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Matching from './components/Match';
import Chat from './components/Chat';
import { HashRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/Match" element={<Matching />} />
        <Route path="/Chat/:matchId" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;
