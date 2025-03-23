import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

function PoliticianCard({ politician }) {
  return (
    <Card sx={{ fontFamily: 'Poppins', width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', mb: 2, backgroundColor: '000', border: '1px solid #eee', borderRadius: 2 }}> {/* Added background color and border */}
      <CardContent sx={{ flexGrow: 1, fontFamily: 'Poppins' }}>
        <Typography variant="h6" component="div" sx={{ fontWeight: 500, fontFamily: 'Poppins' }}> {/* Added font weight */}
          {politician.name}
        </Typography>
        <Typography sx={{ mb: 1.5, color: 'text.secondary', fontWeight: 400, fontFamily: 'Poppins' }}> {/* Added font weight */}
          Party: {politician.party}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default PoliticianCard;
