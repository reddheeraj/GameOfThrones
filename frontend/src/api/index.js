const API_BASE_URL = 'http://localhost:5001/api';

export const runSimulationStep = async () => {
  const response = await fetch(`${API_BASE_URL}/simulate`, { method: 'POST' });
  const data = await response.json();
  return data;
};

export const fetchSimulationState = async () => {
  const response = await fetch(`${API_BASE_URL}/state`);
  const data = await response.json();
  return data;
};

export const fetchPosts = async () => {
  const response = await fetch(`${API_BASE_URL}/posts`);
  const data = await response.json();
  return data;
};
