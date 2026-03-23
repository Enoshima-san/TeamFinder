# Пример проверки JWT 

```js
// api/interceptors.js
import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

// Добавляем access_token к каждому запросу
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Перехватываем 401 и пробуем обновить токен
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Если 401 и запрос ещё не был повторён
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Пытаемся получить новую пару токенов
        const { data } = await axios.post('/auth/refresh', {
          refresh: localStorage.getItem('refresh_token')
        });
        
        // Сохраняем новые токены
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);
        
        // Повторяем исходный запрос с новым access_token
        originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
        return api(originalRequest);
        
      } catch (refreshError) {
        // Refresh не сработал → выходим из аккаунта
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```
