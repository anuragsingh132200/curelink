// Utility functions for local storage

export const getUserId = () => {
  let userId = localStorage.getItem('disha_user_id');

  if (!userId) {
    // Generate a simple UUID
    userId = 'user_' + Math.random().toString(36).substring(2) + Date.now().toString(36);
    localStorage.setItem('disha_user_id', userId);
  }

  return userId;
};

export const clearUserId = () => {
  localStorage.removeItem('disha_user_id');
};
