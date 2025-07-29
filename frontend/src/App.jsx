

import React, { useState } from 'react';
import { Button, TextField, Typography, Box, Paper, CircularProgress, Divider, Tooltip } from '@mui/material';
import SportsEsportsIcon from '@mui/icons-material/SportsEsports';
import FlightIcon from '@mui/icons-material/Flight';
import axios from 'axios';

// Military arcade color palette
const olive = '#3a4d2c';
const darkOlive = '#232d1b';
const khaki = '#bdb76b';
const orange = '#ffb300';
const red = '#e53935';
const green = '#43a047';
const camo = 'repeating-linear-gradient(135deg, #232d1b 0 40px, #3a4d2c 40px 80px, #bdb76b 80px 120px)';

const arcadeStyle = {
  minHeight: '100vh',
  background: camo,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  fontFamily: 'Press Start 2P, monospace',
  letterSpacing: 1.2,
  padding: 0,
  margin: 0,
};

const paperStyle = {
  padding: 14,
  background: 'rgba(35,45,27,0.98)',
  borderRadius: 14,
  boxShadow: `0 0 24px ${khaki}, 0 0 8px ${olive}`,
  border: `3px solid ${khaki}`,
  maxWidth: 340,
  width: '100%',
  position: 'relative',
  overflow: 'hidden',
  minHeight: 420,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'space-between',
};

const inputStyle = {
  marginBottom: 12,
  background: darkOlive,
  borderRadius: 4,
  input: { color: khaki, fontFamily: 'inherit', fontWeight: 700 },
  label: { color: orange, fontFamily: 'inherit' },
};

const buttonStyle = {
  background: `linear-gradient(90deg, ${orange} 0%, ${khaki} 100%)`,
  color: darkOlive,
  fontWeight: 'bold',
  fontFamily: 'inherit',
  fontSize: 17,
  marginTop: 6,
  marginBottom: 4,
  boxShadow: `0 0 8px ${orange}`,
  border: `2px solid ${khaki}`,
  borderRadius: 8,
  transition: 'transform 0.1s',
  '&:active': { transform: 'scale(0.97)' },
};

const neonText = {
  color: orange,
  textShadow: `0 0 6px ${khaki}, 0 0 12px ${orange}`,
  fontFamily: 'inherit',
  fontWeight: 700,
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
      <Paper elevation={10} sx={paperStyle}>
        <Box display="flex" alignItems="center" justifyContent="center" mb={0.5}>
          <SportsEsportsIcon sx={{ fontSize: 28, color: orange, mr: 1, filter: `drop-shadow(0 0 6px ${khaki})` }} />
          <Typography variant="h6" sx={{ color: khaki, fontFamily: 'inherit', fontWeight: 900, letterSpacing: 2, textShadow: `0 0 8px ${khaki}` }}>
            DOGFIGHT
          </Typography>
        </Box>
        <Divider sx={{ bgcolor: orange, mb: 1.2, borderBottomWidth: 2, borderRadius: 2 }} />
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={0.5}>
          <Tooltip title="F16" arrow>
            <FlightIcon sx={{ color: green, fontSize: 22, mr: 1, transform: 'rotate(-10deg)' }} />
          </Tooltip>
          <Typography variant="caption" sx={{ color: khaki, fontFamily: 'inherit', fontWeight: 700, flex: 1, textAlign: 'center', letterSpacing: 1 }}>
            VS
          </Typography>
          <Tooltip title="F18" arrow>
            <FlightIcon sx={{ color: red, fontSize: 22, ml: 1, transform: 'scaleX(-1) rotate(-10deg)' }} />
          </Tooltip>
        </Box>
        <TextField
          label="Distance"
          type="number"
          value={distance}
          onChange={e => setDistance(e.target.value)}
          fullWidth
          sx={inputStyle}
          InputProps={{ style: { color: khaki, fontFamily: 'inherit', fontWeight: 700, fontSize: 13 } }}
          InputLabelProps={{ style: { color: orange, fontFamily: 'inherit', fontSize: 12 } }}
        />
        <TextField
          label="Duration"
          type="number"
          value={duration}
          onChange={e => setDuration(e.target.value)}
          fullWidth
          sx={inputStyle}
          InputProps={{ style: { color: orange, fontFamily: 'inherit', fontWeight: 700, fontSize: 13 } }}
          InputLabelProps={{ style: { color: khaki, fontFamily: 'inherit', fontSize: 12 } }}
        />
        <Button
          variant="contained"
          sx={buttonStyle}
          onClick={handleFight}
          disabled={loading}
          fullWidth
        >
          {loading ? <CircularProgress size={20} sx={{ color: red }} /> : 'FIRE!'}
        </Button>
        {error && (
          <Typography color="error" mt={1} align="center" sx={{ fontSize: 12, fontWeight: 700 }}>
            {error}
          </Typography>
        )}
        {result && (
          <Box mt={1.2}>
            <Typography variant="subtitle2" sx={neonText}>
              Result
            </Typography>
            <pre style={{ color: khaki, background: darkOlive, padding: 8, borderRadius: 7, fontFamily: 'inherit', fontSize: 11, marginTop: 4, border: `1.5px solid ${olive}`, boxShadow: `0 0 6px ${khaki}` }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </Box>
        )}
        <Box sx={{ position: 'absolute', bottom: 4, left: 0, width: '100%', textAlign: 'center', opacity: 0.18 }}>
          <Typography variant="caption" sx={{ color: khaki, fontFamily: 'inherit', fontSize: 9 }}>
            © {new Date().getFullYear()} Dogfight Arcade
          </Typography>
        </Box>
      </Paper>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        html, body, #root { height: 100%; margin: 0; padding: 0; overflow: hidden; }
      `}</style>
    </Box>
  );
}

export default App;
