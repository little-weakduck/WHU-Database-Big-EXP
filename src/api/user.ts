import { instance, type ResponseBody } from './instance';

export const login = (data: { username: string; password: string }) =>
  instance.post('/login', data);
