import React, { useState, useEffect } from 'react';
import './styles/App.css';
import { runSimulationStep, fetchSimulationState, fetchPosts } from './api';
import SocialMediaFeed from './components/SocialMediaFeed';
import CitizenCard from './components/CitizenCard';
import PoliticianCard from './components/PoliticianCard';
import { Container, Grid, Typography, Button, List, ListItem, ListItemText, Paper, Box } from '@mui/material';
import { io } from 'socket.io-client';
import ActionNotification from './components/ActionNotification';

const socket = io('http://localhost:5001');

function App() {
  const [simulationState, setSimulationState] = useState({ citizens: [], politicians: [], vote_counts: {} });
  const [posts, setPosts] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [actionQueue, setActionQueue] = useState([]);

  const loadData = async () => {
    const state = await fetchSimulationState();
    setSimulationState(state);
    const postsData = await fetchPosts();
    setPosts(postsData);
  };

  useEffect(() => {
    loadData();

    const interval = setInterval(() => {
      loadData();
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to WebSocket');
    });

    socket.on('agent_action', (action) => {
      setActionQueue((prevQueue) => [...prevQueue, action]);
    });

    return () => {
      socket.off('connect');
      socket.off('agent_action');
      socket.disconnect();
    };
  }, []);

  const handleRunStep = async () => {
    await runSimulationStep();
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, fontFamily: 'Poppins' }}>
      <Box sx={{ fontFamily: 'Poppins', display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4, p: 2, borderRadius: 2 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ color: 'black', fontWeight: 600, fontFamily: 'Poppins' }}>
          Political Influence Simulator
        </Typography>
        <Paper elevation={3} sx={{ p: 1, width: 'fit-content' }}>
          <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 500, fontFamily: 'Poppins' }}>
            Vote Counts
          </Typography>
          <List dense={true}>
            {Object.entries(simulationState.vote_counts).map(([politician, count]) => (
              <ListItem key={politician} sx={{ py: 0 }}>
                <ListItemText primary={`${politician}: ${count}`} primaryTypographyProps={{ variant: 'body2', fontWeight: 400, fontFamily: 'Poppins' }} />
              </ListItem>
            ))}
          </List>
        </Paper>
      </Box>
      <Button variant="contained" color="primary" onClick={handleRunStep} sx={{ mb: 4, color: 'white', backgroundColor: 'blue', fontFamily: 'Poppins', '&:hover': { backgroundColor: '#367c39' } }}>
        Run Simulation
      </Button>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 500, fontFamily: 'Poppins' }}>
              Citizens
            </Typography>
            <Grid container spacing={2} sx={{display: 'flex', flexWrap: 'wrap', fontFamily: 'Poppins'}}>
              {simulationState.citizens.map((citizen) => (
                <Grid item xs={12} sm={6} md={4} key={citizen.name} sx={{display: 'flex'}}>
                  <CitizenCard citizen={citizen} />
                </Grid>
              ))}
            </Grid>
            <Typography variant="h6" gutterBottom sx={{ mt: 4, fontWeight: 500, fontFamily: 'Poppins' }}>
              Politicians
            </Typography>
            <Grid container spacing={2} sx={{display: 'flex', flexWrap: 'wrap', fontFamily: 'Poppins'}}>
              {simulationState.politicians.map((politician) => (
                <Grid item xs={12} sm={6} md={4} key={politician.name} sx={{display: 'flex', fontFamily: 'Poppins'}}>
                  <PoliticianCard politician={politician} />
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 500, fontFamily: 'Poppins' }}>
              Social Media Feed
            </Typography>
            <SocialMediaFeed posts={posts} />
          </Paper>
        </Grid>
      </Grid>
      {notifications.map((notification, index) => (
        <div key={index} className="notification">
          {notification}
        </div>
      ))}
      <ActionNotification actionQueue={actionQueue} setActionQueue={setActionQueue} />
    </Container>
  );
}

export default App;
