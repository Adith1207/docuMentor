import React, { useState, useEffect } from 'react';
import { Code, MessageSquare, Upload, Download, Trash2, Send, Moon, Sun, FileCode, Sparkles } from 'lucide-react';
import './App.css';

const BASE_URL = 'http://127.0.0.1:8000';

const App = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [activeTab, setActiveTab] = useState('codescribe');
  const [codeFile, setCodeFile] = useState(null);
  const [codeContent, setCodeContent] = useState('');
  const [commentedCode, setCommentedCode] = useState('');
  const [rqaFiles, setRqaFiles] = useState([]);
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAsking, setIsAsking] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [darkMode]);

  const toggleMode = () => setDarkMode(!darkMode);

  const handleCodeFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.name.endsWith('.py')) {
      setCodeFile(file);
      const reader = new FileReader();
      reader.onload = (event) => setCodeContent(event.target.result);
      reader.readAsText(file);
    } else {
      alert('Please upload a .py file');
      setCodeFile(null);
      setCodeContent('');
    }
  };

  const generateComments = async () => {
    if (!codeContent) {
      alert('Please provide code content or upload a file first.');
      return;
    }
    setIsGenerating(true);
    try {
      const response = await fetch(`${BASE_URL}/comment-text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: codeContent }),
      });
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }
      const data = await response.json();
      if (data.status === 'ok') {
        setCommentedCode(data.commented || 'No comments generated.');
      } else {
        throw new Error('Unexpected response from server.');
      }
    } catch (error) {
      console.error('Error generating comments:', error);
      alert(`Failed to generate comments: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadCommentedCode = () => {
    if (!commentedCode || !codeFile) {
      alert('No commented code to download. Generate comments first.');
      return;
    }
    const blob = new Blob([commentedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = codeFile.name.replace('.py', '_commented.py');
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleRqaFileChange = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => file.name.endsWith('.py') || file.name.endsWith('.txt'));
    if (validFiles.length !== files.length) {
      alert('Only .py and .txt files are allowed');
    }
    setRqaFiles(validFiles);
  };

  const createEmbeddings = async () => {
    if (rqaFiles.length === 0) {
      alert('Please select files to create embeddings.');
      return;
    }
    const formData = new FormData();
    rqaFiles.forEach(file => formData.append('files', file));
    try {
      const response = await fetch(`${BASE_URL}/upload-and-embed`, {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      if (data.status === 'ok') {
        alert(data.message);
        setRqaFiles([]);
      }
    } catch (error) {
      console.error('Error creating embeddings:', error);
      alert(`Failed to create embeddings: ${error.message}. Ensure server is running.`);
    }
  };

  const clearEmbeddings = () => {
    window.location.reload()
  };

  const askQuestion = async () => {
    if (!question) {
      alert('Please enter a question.');
      return;
    }
    setIsAsking(true);
    try {
      const response = await fetch(`${BASE_URL}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      if (data.status === 'ok') {
        setChatHistory([...chatHistory, { user: question, bot: data.answer || 'No answer available.' }]);
        setQuestion('');
      }
    } catch (error) {
      console.error('Error asking question:', error);
      alert(`Failed to get answer: ${error.message}. Ensure embeddings are built.`);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'}`}>
      <div className="content-wrapper">
        {/* Header */}
        <header className="app-header">
          <div className="header-content">
            <div className="logo-container">
              <Sparkles size={28} />
            </div>
            <div className="header-text">
              <h1>DocuMENTOR — AI That Stays With You.</h1>
              <p>CodeScribe & LocalRQA Platform</p>
            </div>
          </div>
          <button onClick={toggleMode} className="theme-toggle">
            {darkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </header>

        {/* Tab Navigation */}
        <div className="tab-navigation">
          <button
            onClick={() => setActiveTab('codescribe')}
            className={`tab-button ${activeTab === 'codescribe' ? 'active codescribe-tab' : ''}`}
          >
            <Code size={20} />
            Code Scribe
          </button>
          <button
            onClick={() => setActiveTab('localrqa')}
            className={`tab-button ${activeTab === 'localrqa' ? 'active localrqa-tab' : ''}`}
          >
            <MessageSquare size={20} />
            LocalRQA
          </button>
        </div>

        {/* CodeScribe Tab */}
        {activeTab === 'codescribe' && (
          <div className="tab-content">
            <div className="section-header">
              <FileCode size={24} />
              <h2>Python Code Commenting</h2>
            </div>

            <div className="upload-zone">
              <label className="upload-label">
                <Upload size={32} />
                <span className="upload-text">Click to upload Python file (.py)</span>
                <input
                  type="file"
                  accept=".py"
                  onChange={handleCodeFileChange}
                  className="file-input"
                />
                {codeFile && (
                  <span className="file-name">Selected: {codeFile.name}</span>
                )}
              </label>
            </div>

            {codeContent && (
              <>
                <div className="code-section">
                  <h3>Original Code</h3>
                  <pre className="code-display original-code">
                    {codeContent}
                  </pre>
                </div>

                <button
                  onClick={generateComments}
                  disabled={isGenerating}
                  className={`action-button generate-button ${isGenerating ? 'disabled' : ''}`}
                >
                  <Sparkles size={20} />
                  {isGenerating ? 'Generating...' : 'Generate Comments'}
                </button>

                {commentedCode && (
                  <div className="code-section">
                    <h3>Commented Code</h3>
                    <pre className="code-display commented-code">
                      {commentedCode}
                    </pre>
                    <button onClick={downloadCommentedCode} className="action-button download-button">
                      <Download size={20} />
                      Download Commented File
                    </button>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* LocalRQA Tab */}
        {activeTab === 'localrqa' && (
          <div className="tab-content">
            <div className="section-header">
              <MessageSquare size={24} />
              <h2>Retrieval-Augmented QA</h2>
            </div>

            {/* File Upload Section */}
            <div className="rqa-section">
              <h3>Document Management</h3>
              <div className="upload-zone rqa-upload">
                <label className="upload-label">
                  <Upload size={32} />
                  <span className="upload-text">Upload files for embeddings (.py or .txt)</span>
                  <input
                    type="file"
                    multiple
                    accept=".py,.txt"
                    onChange={handleRqaFileChange}
                    className="file-input"
                  />
                  {rqaFiles.length > 0 && (
                    <span className="file-name">{rqaFiles.length} file(s) selected</span>
                  )}
                </label>
              </div>
              <div className="button-group">
                {rqaFiles.length > 0 && (
                  <button onClick={createEmbeddings} className="action-button upload-button">
                    <Upload size={20} />
                    Create Embeddings
                  </button>
                )}
                <button onClick={clearEmbeddings} className="action-button delete-button">
                  <Trash2 size={20} />
                  Clear Embeddings
                </button>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="chat-section">
              <h3>Chat Interface</h3>
              <div className="chat-history">
                {chatHistory.length === 0 ? (
                  <div className="empty-chat">
                    <p>No messages yet. Start a conversation!</p>
                  </div>
                ) : (
                  chatHistory.map((msg, index) => (
                    <div key={index} className="message-group">
                      <div className="message user-message">
                        <p className="message-sender">You</p>
                        <p className="message-text">{msg.user}</p>
                      </div>
                      <div className="message bot-message">
                        <p className="message-sender">Assistant</p>
                        <p className="message-text">{msg.bot}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
              <div className="chat-input-container">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && askQuestion()}
                  placeholder="Ask a question about your documents..."
                  className="chat-input"
                />
                <button
                  onClick={askQuestion}
                  disabled={isAsking}
                  className={`action-button send-button ${isAsking ? 'disabled' : ''}`}
                >
                  <Send size={20} />
                  {isAsking ? 'Sending...' : 'Send'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;