import React, { useState } from 'react';
import Box from '@mui/material/Box';
import {
  Button,
  List,
  ListItemButton,
  ListItemText,
  Typography,
  Slider,
} from '@mui/material';
import ReactAudioPlayer from 'react-audio-player';
import Axios from 'axios';
import { ThemeProvider, createTheme } from '@mui/material/styles';

import './App.css';
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});
const BACKEND_URI = 'http://localhost:8000';

function App() {
  const [songSelectedIndex, setSongSelectedIndex] = useState(0);
  const [songData, setSongData] = useState([]);
  const [pitchValue, setPitchValue] = useState(0);
  const [speedValue, setSpeedValue] = useState(1);
  const [noiseValue, setNoiseValue] = useState(1);

  let songs = [
    {
      title: 'Blinding Lights',
      artist: 'The Weeknd',
      id: 0,
    },
    {
      title: 'Moth to a Flame',
      artist: 'The Weeknd',
      id: 1,
    },
  ];

  const handleListItemClick = (event, index) => {
    setSongSelectedIndex(index);
  };

  const handleGenerateSong = async (event) => {
    let res = await Axios.post(`${BACKEND_URI}/generate-song`, {
      song: songs[songSelectedIndex],
      pitch: pitchValue,
      speed: speedValue,
      noise: noiseValue,
    });
    setSongData(res.data.song);
  };

  const handlePredictSong = async (event) => {
    let res = await Axios.post(`${BACKEND_URI}/predict-song`, {
      data: songData,
    });
    let songID = res.data.id;
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <div className="App">
        <div className="left">
          <Typography variant="h3">Song Classification</Typography>
          <div className="select">
            {/* Song select */}
            <Typography variant="h4" align="left">
              Select a song:
            </Typography>
            <Box
              sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}
            >
              <List component="nav" aria-label="secondary mailbox folder">
                {songs.map((song, i) => (
                  <ListItemButton
                    selected={songSelectedIndex === i}
                    onClick={(event) => handleListItemClick(event, i)}
                    key={i}
                  >
                    <ListItemText primary={song.title} />
                  </ListItemButton>
                ))}
              </List>
            </Box>

            {/* Pitch */}
            <Typography variant="h4" align="left">
              Augment Pitch
            </Typography>
            <Slider
              defaultValue={0}
              min={-12}
              max={12}
              valueLabelDisplay="auto"
              onChange={(event) => {
                setPitchValue(event.target.value);
              }}
            />

            {/* Speed */}
            <Typography variant="h4" align="left">
              Augment Speed
            </Typography>
            <Slider
              defaultValue={1}
              min={0.8}
              max={1.5}
              step={0.1}
              valueLabelDisplay="auto"
              onChange={(event) => {
                setSpeedValue(event.target.value);
              }}
            />

            {/* Speed */}
            <Typography variant="h4" align="left">
              Augment Noise
            </Typography>
            <Slider
              defaultValue={0.05}
              min={0}
              max={0.1}
              step={0.025}
              valueLabelDisplay="auto"
              onChange={(event) => {
                setNoiseValue(event.target.value);
              }}
            />

            <Button
              variant="contained"
              onClick={(event) => handleGenerateSong(event)}
            >
              Generate
            </Button>
          </div>
        </div>
        <div className="right">
          {/* Hear augmented song */}
          {songData.length > 0 && (
            <div>
              <Typography variant="h3">Augmented Song</Typography>
              <div className="audioPlayer">
                <ReactAudioPlayer
                  src={`${BACKEND_URI}/file/song.ogg`}
                  autoplay
                  controls
                />
              </div>
              <Button
                variant="contained"
                onClick={(event) => handlePredictSong(event)}
              >
                Predict
              </Button>
            </div>
          )}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
