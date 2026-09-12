import React, { useState } from 'react';
import { api } from '../api/client';
import { Bot, Send, Sparkles, ShieldAlert, BookOpen, User } from 'lucide-react';

interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
  sources?: any[];
  timestamp: string;
}

export const AiAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: 'ai',
      text: "Hello! I am the SiteFlow AI Project Assistant. You can ask me questions regarding contract BOQ rates, remaining quantities, project assumptions (5 Marla, 750 sq.ft.), active check requests, or site observations. Note that all answers are derived strictly from authoritative project data.",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [isThinking, setIsThinking] = useState(false);

  const sampleQueries = [
    "What is the remaining quantity for masonry?",
    "What is the contract rate for RCC?",
    "Which inspections are pending?",
    "What is the total contract value and budget?",
    "What was the latest observation recorded?"
  ];

  const handleSend = async (queryText?: string) => {
    const q = queryText || inputQuery;
    if (!q.trim() || isThinking) return;

    const userMsg: ChatMessage = {
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setIsThinking(true);

    try {
      const res = await api.queryRag(q);
      const aiMsg: ChatMessage = {
        sender: 'ai',
        text: res.answer,
        sources: res.sources,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (e: any) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: "I encountered an error querying project knowledge: " + (e.message || "Unknown error"),
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Bot color="#38bdf8" size={28} /> SiteFlow RAG Knowledge Assistant
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.86rem' }}>
            Interactive conversational retrieval across BOQ, Takeoff, Site Specifications & Audit Records
          </p>
        </div>

        <span className="ai-badge">Advisory Knowledge Retrieval</span>
      </div>

      {/* Suggested Prompt Chips */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '12px', marginBottom: '16px' }}>
        {sampleQueries.map((sq, idx) => (
          <button
            key={idx}
            type="button"
            className="btn btn-secondary btn-sm"
            style={{ fontSize: '0.76rem', whiteSpace: 'nowrap', borderRadius: 'var(--radius-full)' }}
            onClick={() => handleSend(sq)}
          >
            <Sparkles size={12} color="#38bdf8" /> {sq}
          </button>
        ))}
      </div>

      {/* Chat Messages Container */}
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-color)',
        borderRadius: 'var(--radius-lg)',
        height: '520px',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {messages.map((m, idx) => (
            <div
              key={idx}
              style={{
                display: 'flex',
                gap: '12px',
                alignItems: 'flex-start',
                alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%'
              }}
            >
              {m.sender === 'ai' && (
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'rgba(56, 189, 248, 0.15)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  <Bot size={18} color="#38bdf8" />
                </div>
              )}

              <div style={{
                background: m.sender === 'user' ? '#0284c7' : '#131c2e',
                color: '#fff',
                padding: '12px 16px',
                borderRadius: 'var(--radius-md)',
                fontSize: '0.88rem',
                border: m.sender === 'ai' ? '1px solid var(--border-color)' : 'none',
                lineHeight: 1.5,
                whiteSpace: 'pre-wrap'
              }}>
                <div>{m.text}</div>

                {m.sources && m.sources.length > 0 && (
                  <div style={{ marginTop: '10px', paddingTop: '8px', borderTop: '1px solid #1e293b', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    {m.sources.map((s: any, sIdx: number) => (
                      <span key={sIdx} style={{
                        fontSize: '0.68rem',
                        background: '#1e293b',
                        color: 'var(--primary)',
                        padding: '2px 8px',
                        borderRadius: 'var(--radius-sm)',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}>
                        <BookOpen size={10} /> {s.title}
                      </span>
                    ))}
                  </div>
                )}

                <div style={{ fontSize: '0.65rem', color: m.sender === 'user' ? 'rgba(255, 255, 255, 0.7)' : 'var(--text-dim)', textAlign: 'right', marginTop: '4px' }}>
                  {m.timestamp}
                </div>
              </div>

              {m.sender === 'user' && (
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'rgba(245, 158, 11, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0
                }}>
                  <User size={18} color="#fbbf24" />
                </div>
              )}
            </div>
          ))}

          {isThinking && (
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center', color: 'var(--text-dim)', fontSize: '0.82rem' }}>
              <Bot size={18} color="#38bdf8" />
              <span>Retrieving project context & validating facts...</span>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          style={{
            padding: '14px 20px',
            borderTop: '1px solid var(--border-color)',
            display: 'flex',
            gap: '12px',
            background: '#0c1322',
            borderBottomLeftRadius: 'var(--radius-lg)',
            borderBottomRightRadius: 'var(--radius-lg)'
          }}
        >
          <input
            type="text"
            className="form-input"
            placeholder="Ask anything about rates, remaining quantities, check requests..."
            style={{ flex: 1 }}
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
          />
          <button type="submit" className="btn btn-primary" disabled={isThinking || !inputQuery.trim()}>
            <Send size={16} /> Send
          </button>
        </form>
      </div>
    </div>
  );
};
