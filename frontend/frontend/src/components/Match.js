import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Match() {
  const [message, setMessage] = useState(''); // 顯示配對訊息
  const [isMatching, setIsMatching] = useState(false); // 控制配對狀態
  const username = sessionStorage.getItem('username'); // 從 sessionStorage 獲取使用者名稱
  const navigate = useNavigate();

  // 進行配對
  const handleMatch = async () => {
    setIsMatching(true); // 設定為配對中
    setMessage('等待配對中...');

    try {
      const response = await fetch('http://localhost:8050/api/match/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`配對成功！配對對象: ${data.match_id}`);
        navigate(`/Chat/${data.match_id}`); // 配對成功後導向聊天頁面
      } else {
        setMessage(data.message || '配對失敗');
        setIsMatching(false); // 恢復按鈕狀態
      }
    } catch (error) {
      console.error('配對請求失敗:', error);
      setMessage('配對請求失敗');
      setIsMatching(false); // 發生錯誤時恢復狀態
    }
  };

  // 取消配對
  const handleCancelMatch = async () => {
    try {
      const response = await fetch('http://localhost:8050/api/cancel-match/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(data.message); // 顯示取消成功訊息
        setIsMatching(false); // 恢復按鈕狀態
      } else {
        setMessage(data.message || '取消配對失敗');
      }
    } catch (error) {
      console.error('取消配對請求失敗:', error);
      setMessage('取消配對請求失敗');
    }
  };

  return (
    <div>
      <h1>配對頁面</h1>
      {isMatching ? (
        <>
          <p>配對進行中...</p>
          <button onClick={handleCancelMatch}>取消配對</button>
        </>
      ) : (
        <button onClick={handleMatch}>開始配對</button>
      )}
      <p>{message}</p>
    </div>
  );
}

export default Match;
