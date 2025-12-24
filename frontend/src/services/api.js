import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  getUser: async (userId) => {
    const response = await api.get(`/api/chat/user/${userId}`);
    return response.data;
  },

  initializeChat: async (userId) => {
    const response = await api.post(`/api/chat/user/${userId}/initialize`);
    return response.data;
  },

  getMessages: async (userId, page = 1, perPage = 20) => {
    const response = await api.get(`/api/chat/user/${userId}/messages`, {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  sendMessage: async (userId, content) => {
    const response = await api.post(`/api/chat/user/${userId}/message`, {
      content,
    });
    return response.data;
  },
};

export default api;
