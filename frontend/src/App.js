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
import SongCard from './components/SongCard';

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
  const [songAugmentation, setSongAugmentation] = useState({});
  const [pitchValue, setPitchValue] = useState(0);
  const [speedValue, setSpeedValue] = useState(1);
  const [noiseValue, setNoiseValue] = useState(0.015);
  const [predictedSongId, setPredictedSongId] = useState(-1);
  const [predictedSongMetadata, setPredictedSongMetadata] = useState({});

  let songs = [
    {
      title: '7 rings',
      artist: 'Ariana Grande',
      id: 1450330685,
    },
    {
      title: 'God is a woman',
      artist: 'Ariana Grande',
      id: 1399202954,
    },
    // {
    //   title: 'As It Was',
    //   artist: 'Harry Styles',
    //   id: 1615585008,
    // },
    // {
    //   title: 'Watermelon Sugar',
    //   artist: 'Harry Styles',
    //   id: 1485802967,
    // },
    {
      title: 'Hold On',
      artist: 'Justin Bieber',
      id: 1561058477,
    },
    {
      title: 'Intentions (feat. Quavo)',
      artist: 'Justin Bieber',
      id: 1496639586,
    },
    {
      title: 'STAY',
      artist: 'The Kid LAROI',
      id: 1574378625,
    },
    {
      title: 'BEST FOR ME',
      artist: 'The Kid LAROI',
      id: 1578326275,
    },
    {
      title: 'In Your Eyes',
      artist: 'The Weeknd',
      id: 1499378612,
    },
    {
      title: 'Die For You',
      artist: 'The Weeknd',
      id: 1440872304,
    },
  ];

  const handleListItemClick = (event, index) => {
    setSongSelectedIndex(index);
  };

  const handleGenerateSong = async (event) => {
    setSongAugmentation({});
    setPredictedSongId(-1);
    let augmentation = {
      song: songs[songSelectedIndex],
      pitch: pitchValue,
      speed: speedValue,
      noise: noiseValue,
    };
    let res = await Axios.post(`${BACKEND_URI}/generate-song`, augmentation);
    if (res.status === 200) {
      augmentation['isAugmented'] = true;
      setSongAugmentation(augmentation);
    }
  };

  const handlePredictSong = async (event) => {
    // let res = await Axios.post(`${BACKEND_URI}/predict-song`, {
    //   song: songs[songSelectedIndex],
    //   pitch: pitchValue,
    //   speed: speedValue,
    //   noise: noiseValue,
    // });
    // let songId = res.data.song_id;
    // res = await Axios.get(`${BACKEND_URI}/song-meta?song_id=${songId}`);
    // const { artistName, artworkUrl100, trackName, trackViewUrl } =
    //   res.data.results[0];
    // setPredictedSongMetadata({
    //   artistName,
    //   artworkUrl100,
    //   trackName,
    //   trackViewUrl,
    // });
    // setPredictedSongId(songId);
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
              defaultValue={0.015}
              min={0}
              max={0.03}
              step={0.005}
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
          {songAugmentation.isAugmented === true && (
            <div>
              <Typography variant="h3">Augmented Song</Typography>
              <div className="audioPlayer">
                <ReactAudioPlayer
                  src={`${BACKEND_URI}/files/${songAugmentation.song.id}-${
                    songAugmentation.pitch
                  }-${songAugmentation.speed.toFixed(
                    1
                  )}-${songAugmentation.noise.toFixed(3)}.ogg`}
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
          {predictedSongId >= 0 && (
            <div>
              <Typography variant="h3" sx={{ marginTop: '30px' }}>
                Predicted Song
              </Typography>
              <SongCard
                artistName={predictedSongMetadata.artistName}
                artworkUrl100={predictedSongMetadata.artworkUrl100}
                trackName={predictedSongMetadata.trackName}
                trackViewUrl={predictedSongMetadata.trackViewUrl}
              />
            </div>
          )}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
