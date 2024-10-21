// src/FriendsList.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Typography, Button, List, ListItem, ListItemText, Box, Paper } from '@mui/material'; // 引入 MUI 元件

function FriendsList() {
  const [friends, setFriends] = useState([]);
  const username = sessionStorage.getItem('username');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFriends = async () => {
      try {
        const response = await fetch(`http://localhost:8050/api/friends/?username=${username}`);
        const data = await response.json();
        if (response.ok) {
          setFriends(data.friends);
        } else {
          console.error('[ERROR] 獲取好友列表失敗:', data);
        }
      } catch (error) {
        console.error('[ERROR] 發生錯誤:', error);
      }
    };
    fetchFriends();
  }, [username]);

  // const handleChat = (friendUsername) => {
  //   // 點擊好友開始聊天的邏輯
  //   // 可以導航到聊天頁面，並傳遞匹配 ID 或好友資訊
  //   navigate(`/chat-with-friend/${friendUsername}`);
  // };
  const handleChat = (friendUsername) => {
    navigate(`/Chat/${friendUsername}`, { state: { friendUsername } }); // 導航並傳遞好友名稱
  };

//   return (
//     <div>
//       <h2>好友列表</h2>
//       {friends.length > 0 ? (
//         <ul>
//           {friends.map((friend, index) => (
//             <li key={index}>
//               {friend}
//               <button onClick={() => handleChat(friend)}>聊天</button>
//             </li>
//           ))}
//         </ul>
//       ) : (
//         <p>您還沒有好友。</p>
//       )}
//     </div>
//   );
// }

// export default FriendsList;
return (
  <Box
    display="flex"
    flexDirection="column"
    alignItems="center"
    justifyContent="center"
    padding={2}
    minHeight="100vh"
  >
    <Typography variant="h4" gutterBottom>
      好友列表
    </Typography>

    <Paper elevation={3} sx={{ width: '100%', maxWidth: 600, padding: 2 }}>
      {friends.length > 0 ? (
        <List>
          {friends.map((friend, index) => (
            <ListItem key={index} sx={{ justifyContent: 'space-between' }}>
              <ListItemText primary={friend} />
              <Button
                variant="contained"
                color="primary"
                onClick={() => handleChat(friend)}
              >
                聊天
              </Button>
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography variant="body1" color="textSecondary">
          您還沒有好友。
        </Typography>
      )}
    </Paper>
  </Box>
);
}

export default FriendsList;
