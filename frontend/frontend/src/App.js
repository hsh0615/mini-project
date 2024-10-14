
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
