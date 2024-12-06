import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import About from './components/About'; // Example additional page
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>MindCare Companion</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Chatbot />} />
            <Route path="/about" element={<About />} /> {/* Example additional route */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
