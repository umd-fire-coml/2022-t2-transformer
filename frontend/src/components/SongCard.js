import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

export default function SongCard({
  artistName,
  artworkUrl100,
  trackName,
  trackViewUrl,
}) {
  return (
    <Card sx={{ display: 'flex', margin: '10px auto', width: '400px' }}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Typography component="div" variant="h5">
            {trackName}
          </Typography>
          <Typography
            variant="subtitle1"
            color="text.secondary"
            component="div"
          >
            {artistName}
          </Typography>
        </CardContent>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            pl: 1,
            pb: 1,
          }}
        >
          <IconButton
            aria-label="track url"
            href={trackViewUrl}
            target="_blank"
          >
            <OpenInNewIcon />
          </IconButton>
        </Box>
      </Box>
      <CardMedia
        component="img"
        sx={{ width: 151, height: 151 }}
        image={artworkUrl100}
        alt="artwork"
      />
    </Card>
  );
}
