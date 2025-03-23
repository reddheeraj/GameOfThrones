import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

function SocialMediaFeed({ posts }) {
  return (
    <Box
      sx={{
        height: '1000px', // Increased height for the scrollable area
        overflowY: 'auto', // Enable vertical scrolling
        overflowX: 'hidden', // Hide horizontal scrolling
        border: '2px solid #ccc',
        borderRadius: '5px',
        padding: '0',
      }}
    >
      <div className="social-media-feed">
        {posts.map((post, index) => (
          <Paper key={index} elevation={2} sx={{fontFamily: 'Poppins',  p: 2, mb: 2, backgroundColor: '#f8f8f8', border: '1px solid #eee', borderRadius: 2 }}> {/* Added background color and border */}
            <div className="post-header">
              <Typography variant="subtitle1" component="span" className="post-author" sx={{ fontFamily: 'Poppins', fontWeight: 500 }}> {/* Added font weight */}
                {post.metadata.name}
              </Typography>
              <Typography variant="caption" component="span" className="post-date" sx={{ fontFamily: 'Poppins', ml: 1, fontWeight: 300 }}> {/* Added font weight */}
                {post.metadata.date_time}
              </Typography>
            </div>
            <div className="post-content">
              <Typography variant="body1" sx={{ fontWeight: 400, fontFamily: 'Poppins' }}>{post.content}</Typography> {/* Added font weight */}
            </div>
          </Paper>
        ))}
      </div>
    </Box>
  );
}

export default SocialMediaFeed;
