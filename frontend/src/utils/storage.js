// Utility functions for local storage

// Generate a valid UUID v4
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

// Check if a string is a valid UUID
const isValidUUID = (str) => {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(str);
};

export const getUserId = () => {
  let userId = localStorage.getItem('disha_user_id');

  // If userId exists but is not a valid UUID, generate a new one
  if (userId && !isValidUUID(userId)) {
    console.log('Migrating old user ID format to UUID');
    userId = null;
  }

  if (!userId) {
    // Generate a valid UUID v4
    userId = generateUUID();
    localStorage.setItem('disha_user_id', userId);
  }

  return userId;
};

export const clearUserId = () => {
  localStorage.removeItem('disha_user_id');
};
