import './App.css';
import { useState } from 'react';
import PredictionForm from './components/PredictionForm.jsx';
import Results from './components/Results.jsx';

function App() {
  const [sleepScore, setSleepScore] = useState(null);

  return (
    <div className="app-container">
      <PredictionForm onScoreCalculated={setSleepScore} />
      <Results score={sleepScore} />
    </div>
  );
}

export default App;
