import React, { useState } from 'react';
import { Button, TextField, Typography, Box, Paper, CircularProgress } from '@mui/material';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import axios from 'axios';

const arcadeStyle = {
  minHeight: '100vh',
  background: 'radial-gradient(circle at 50% 30%, #2e2e2e 60%, #181818 100%)',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  fontFamily: 'Press Start 2P, monospace',
};

const paperStyle = {
  padding: 32,
  background: '#232323',
  borderRadius: 16,
  boxShadow: '0 0 24px #00ffe7, 0 0 8px #ff00c8',
  border: '2px solid #00ffe7',
  maxWidth: 400,
  width: '100%',
};

const inputStyle = {
  marginBottom: 24,
  background: '#181818',
  borderRadius: 4,
};

const buttonStyle = {
  background: 'linear-gradient(90deg, #00ffe7 0%, #ff00c8 100%)',
  color: '#181818',
  fontWeight: 'bold',
  fontFamily: 'inherit',
  fontSize: 18,
  marginTop: 16,
  boxShadow: '0 0 8px #00ffe7',
};

function App() {
  const [distance, setDistance] = useState('500');
  const [duration, setDuration] = useState('5');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFight = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      // Change the URL below if your backend is not on localhost:8000
      const res = await axios.get(
        `http://localhost:8000/dogfight/exchange/${distance}/${duration}`
      );
      setResult(res.data);
    } catch (err) {
      setError('Failed to fetch result. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={arcadeStyle}>
      <Paper elevation={8} sx={paperStyle}>
        <Box display="flex" alignItems="center" justifyContent="center" mb={2}>
          <SportsEsportsIcon sx={{ fontSize: 40, color: '#00ffe7', mr: 1 }} />
          <Typography variant="h4" sx={{ color: '#ff00c8', fontFamily: 'inherit' }}>
            Dogfight Arcade
          </Typography>
        </Box>
        <TextField
          label="Distance"
          type="number"
          value={distance}
          onChange={e => setDistance(e.target.value)}
          fullWidth
          sx={inputStyle}
          InputProps={{ style: { color: '#00ffe7', fontFamily: 'inherit' } }}
          InputLabelProps={{ style: { color: '#ff00c8', fontFamily: 'inherit' } }}
        />
        <TextField
          label="Duration"
          type="number"
          value={duration}
          onChange={e => setDuration(e.target.value)}
          fullWidth
          sx={inputStyle}
          InputProps={{ style: { color: '#00ffe7', fontFamily: 'inherit' } }}
          InputLabelProps={{ style: { color: '#ff00c8', fontFamily: 'inherit' } }}
        />
        <Button
          variant="contained"
          sx={buttonStyle}
          onClick={handleFight}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={24} sx={{ color: '#ff00c8' }} /> : 'FIGHT!'}
        </Button>
        {error && (
          <Typography color="error" mt={2} align="center">
            {error}
          </Typography>
        )}
        {result && (
          <Box mt={3}>
            <Typography variant="h6" sx={{ color: '#00ffe7', fontFamily: 'inherit' }}>
              Result
            </Typography>
            <pre style={{ color: '#fff', background: '#181818', padding: 12, borderRadius: 8, fontFamily: 'inherit', fontSize: 13 }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </Box>
        )}
      </Paper>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
      `}</style>
    </Box>
  );
}

export default App;
