import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function CitizenCard({ citizen }) {
  return (
    <Card sx={{ fontFamily: 'Poppins', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', mb: 2, backgroundColor: '#f8f8f8', border: '1px solid #eee', borderRadius: 2 }}> {/* Added background color and border */}
      <CardContent sx={{ flexGrow: 1, fontFamily: 'Poppins'}}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 500, fontFamily: 'Poppins' }}> {/* Added font weight */}
          {citizen.name}
        </Typography>
        <Typography sx={{ mb: 1.5, color: 'text.secondary', fontWeight: 400, fontFamily: 'Poppins' }}> {/* Added font weight */}
          Vote: {citizen.vote}
        </Typography>
        <Typography variant="body2" sx={{ fontWeight: 300, fontFamily: 'Poppins' }}> {/* Added font weight */}
            {citizen.memory && citizen.memory.length > 0 && citizen.memory[0]['because'] ? JSON.stringify(citizen.memory[0]['because']) : "No memory yet"}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default CitizenCard;
