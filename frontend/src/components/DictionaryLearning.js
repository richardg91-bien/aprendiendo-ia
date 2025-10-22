import React, { useState, useEffect } from 'react';

const DictionaryLearning = () => {
  const [learningStats, setLearningStats] = useState({
    total_words: 0,
    words_learned_today: 0,
    learning_enabled: false,
    last_session: {
      date: null,
      words_learned: 0,
      success_rate: 0
    }
  });
  
  const [isLearning, setIsLearning] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedWord, setSelectedWord] = useState(null);
  const [newWord, setNewWord] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchLearningStats();
    const interval = setInterval(fetchLearningStats, 30000); // Actualizar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchLearningStats = async () => {
    try {
      const response = await fetch('/api/dictionary/stats');
      const data = await response.json();
      if (data.success) {
        setLearningStats(data.stats);
        setIsLearning(data.stats.learning_enabled);
      }
    } catch (error) {
      console.error('Error fetching learning stats:', error);
    }
  };

  const toggleLearning = async () => {
    setLoading(true);
    try {
      const endpoint = isLearning ? '/api/dictionary/stop-learning' : '/api/dictionary/start-learning';
      const response = await fetch(endpoint, { method: 'POST' });
      const data = await response.json();
      
      if (data.success) {
        setIsLearning(!isLearning);
        fetchLearningStats();
      } else {
        alert('Error: ' + data.message);
      }
    } catch (error) {
      console.error('Error toggling learning:', error);
      alert('Error de conexión');
    }
    setLoading(false);
  };

  const searchWords = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await fetch(`/api/dictionary/search?q=${encodeURIComponent(query)}&limit=10`);
      const data = await response.json();
      if (data.success) {
        setSearchResults(data.results);
      }
    } catch (error) {
      console.error('Error searching words:', error);
    }
  };

  const getWordDefinition = async (word) => {
    try {
      const response = await fetch(`/api/dictionary/word/${encodeURIComponent(word)}`);
      const data = await response.json();
      if (data.success) {
        setSelectedWord(data.word_data);
      } else {
        alert('Palabra no encontrada');
      }
    } catch (error) {
      console.error('Error getting word definition:', error);
    }
  };

  const learnNewWord = async () => {
    if (!newWord.trim()) return;

    setLoading(true);
    try {
      const response = await fetch('/api/dictionary/learn-word', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ word: newWord.trim() })
      });
      
      const data = await response.json();
      if (data.success) {
        alert(`Palabra "${newWord}" aprendida exitosamente`);
        setNewWord('');
        fetchLearningStats();
      } else {
        alert('Error: ' + data.message);
      }
    } catch (error) {
      console.error('Error learning word:', error);
      alert('Error de conexión');
    }
    setLoading(false);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Nunca';
    return new Date(dateString).toLocaleString('es-ES');
  };

  return (
    <div className="dictionary-learning">
      <div className="card">
        <div className="card-header">
          <h3>📚 Sistema de Aprendizaje de Diccionario</h3>
        </div>
        
        <div className="card-body">
          {/* Estadísticas */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">{learningStats.total_words}</div>
              <div className="stat-label">Palabras Totales</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">{learningStats.words_learned_today}</div>
              <div className="stat-label">Aprendidas Hoy</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">
                {learningStats.last_session.success_rate 
                  ? (learningStats.last_session.success_rate * 100).toFixed(1) + '%'
                  : '0%'}
              </div>
              <div className="stat-label">Tasa de Éxito</div>
            </div>
          </div>

          {/* Control de Aprendizaje */}
          <div className="learning-control">
            <button
              onClick={toggleLearning}
              disabled={loading}
              className={`btn ${isLearning ? 'btn-danger' : 'btn-success'}`}
            >
              {loading ? '⏳ Procesando...' : (isLearning ? '⏹️ Detener Aprendizaje' : '▶️ Iniciar Aprendizaje')}
            </button>
            
            <div className="status">
              Estado: <span className={isLearning ? 'status-active' : 'status-inactive'}>
                {isLearning ? '🟢 Activo' : '🔴 Inactivo'}
              </span>
            </div>
          </div>

          {/* Última Sesión */}
          {learningStats.last_session.date && (
            <div className="last-session">
              <h4>📊 Última Sesión</h4>
              <p>📅 Fecha: {formatDate(learningStats.last_session.date)}</p>
              <p>📖 Palabras aprendidas: {learningStats.last_session.words_learned}</p>
              <p>✅ Tasa de éxito: {(learningStats.last_session.success_rate * 100).toFixed(1)}%</p>
            </div>
          )}

          {/* Buscar Palabras */}
          <div className="search-section">
            <h4>🔍 Buscar Palabras</h4>
            <div className="search-input">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  searchWords(e.target.value);
                }}
                placeholder="Buscar palabras en el diccionario..."
                className="form-control"
              />
            </div>
            
            {searchResults.length > 0 && (
              <div className="search-results">
                {searchResults.map((result, index) => (
                  <div
                    key={index}
                    className="search-result-item"
                    onClick={() => getWordDefinition(result.word)}
                  >
                    <strong>{result.word}</strong> ({result.part_of_speech})
                    <p>{result.definition.substring(0, 100)}...</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Definición de Palabra Seleccionada */}
          {selectedWord && (
            <div className="word-definition">
              <h4>📖 Definición</h4>
              <div className="word-card">
                <h5>{selectedWord.word.toUpperCase()}</h5>
                {selectedWord.pronunciation && (
                  <p className="pronunciation">[{selectedWord.pronunciation}]</p>
                )}
                <p className="part-of-speech">({selectedWord.part_of_speech})</p>
                <p className="definition">{selectedWord.definition}</p>
                
                {selectedWord.example && (
                  <div className="example">
                    <strong>Ejemplo:</strong> {selectedWord.example}
                  </div>
                )}
                
                {selectedWord.synonyms && (
                  <div className="synonyms">
                    <strong>Sinónimos:</strong> {selectedWord.synonyms}
                  </div>
                )}
                
                {selectedWord.antonyms && (
                  <div className="antonyms">
                    <strong>Antónimos:</strong> {selectedWord.antonyms}
                  </div>
                )}
                
                <div className="confidence">
                  Confianza: {(selectedWord.confidence * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          )}

          {/* Aprender Nueva Palabra */}
          <div className="learn-word-section">
            <h4>➕ Aprender Nueva Palabra</h4>
            <div className="learn-word-input">
              <input
                type="text"
                value={newWord}
                onChange={(e) => setNewWord(e.target.value)}
                placeholder="Escribe una palabra para aprender..."
                className="form-control"
                onKeyPress={(e) => e.key === 'Enter' && learnNewWord()}
              />
              <button
                onClick={learnNewWord}
                disabled={loading || !newWord.trim()}
                className="btn btn-primary"
              >
                {loading ? '⏳' : '📚 Aprender'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .dictionary-learning {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }

        .card {
          background: white;
          border-radius: 10px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          overflow: hidden;
        }

        .card-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          text-align: center;
        }

        .card-header h3 {
          margin: 0;
          font-size: 1.5rem;
        }

        .card-body {
          padding: 20px;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 15px;
          margin-bottom: 20px;
        }

        .stat-card {
          background: #f8f9fa;
          padding: 15px;
          border-radius: 8px;
          text-align: center;
          border: 1px solid #e9ecef;
        }

        .stat-number {
          font-size: 2rem;
          font-weight: bold;
          color: #495057;
        }

        .stat-label {
          font-size: 0.9rem;
          color: #6c757d;
          margin-top: 5px;
        }

        .learning-control {
          display: flex;
          align-items: center;
          gap: 20px;
          margin-bottom: 20px;
          padding: 15px;
          background: #f8f9fa;
          border-radius: 8px;
        }

        .btn {
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          font-weight: bold;
          transition: all 0.3s;
        }

        .btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-success {
          background: #28a745;
          color: white;
        }

        .btn-success:hover:not(:disabled) {
          background: #218838;
        }

        .btn-danger {
          background: #dc3545;
          color: white;
        }

        .btn-danger:hover:not(:disabled) {
          background: #c82333;
        }

        .btn-primary {
          background: #007bff;
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          background: #0056b3;
        }

        .status-active {
          color: #28a745;
          font-weight: bold;
        }

        .status-inactive {
          color: #dc3545;
          font-weight: bold;
        }

        .last-session {
          background: #e7f3ff;
          padding: 15px;
          border-radius: 8px;
          margin-bottom: 20px;
          border-left: 4px solid #007bff;
        }

        .last-session h4 {
          margin-top: 0;
          color: #0056b3;
        }

        .last-session p {
          margin: 5px 0;
        }

        .search-section, .learn-word-section {
          margin-bottom: 20px;
        }

        .search-section h4, .learn-word-section h4 {
          color: #495057;
          margin-bottom: 10px;
        }

        .form-control {
          width: 100%;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 5px;
          font-size: 1rem;
        }

        .search-results {
          max-height: 300px;
          overflow-y: auto;
          border: 1px solid #ddd;
          border-radius: 5px;
          margin-top: 10px;
        }

        .search-result-item {
          padding: 10px;
          border-bottom: 1px solid #eee;
          cursor: pointer;
          transition: background 0.2s;
        }

        .search-result-item:hover {
          background: #f8f9fa;
        }

        .search-result-item:last-child {
          border-bottom: none;
        }

        .search-result-item strong {
          color: #007bff;
        }

        .search-result-item p {
          margin: 5px 0 0 0;
          color: #6c757d;
          font-size: 0.9rem;
        }

        .word-definition {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
        }

        .word-card {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .word-card h5 {
          color: #007bff;
          font-size: 1.5rem;
          margin: 0 0 10px 0;
        }

        .pronunciation {
          font-style: italic;
          color: #6c757d;
          margin: 0;
        }

        .part-of-speech {
          font-weight: bold;
          color: #495057;
          margin: 5px 0;
        }

        .definition {
          font-size: 1.1rem;
          line-height: 1.6;
          margin: 15px 0;
        }

        .example, .synonyms, .antonyms {
          margin: 10px 0;
          padding: 10px;
          background: #f8f9fa;
          border-radius: 5px;
        }

        .confidence {
          text-align: right;
          font-size: 0.9rem;
          color: #6c757d;
          margin-top: 15px;
        }

        .learn-word-input {
          display: flex;
          gap: 10px;
        }

        .learn-word-input input {
          flex: 1;
        }

        .learn-word-input button {
          white-space: nowrap;
        }

        @media (max-width: 768px) {
          .learning-control {
            flex-direction: column;
            align-items: stretch;
          }

          .learn-word-input {
            flex-direction: column;
          }

          .stats-grid {
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          }
        }
      `}</style>
    </div>
  );
};

export default DictionaryLearning;