import { instance, type ResponseBody } from './instance';

export const login = (data: { username: string; password: string }) =>
  instance.post<{ name: string; usertype: 0 | 1 }>('/login', data);

export const register = (data: { username: string; password: string; usertype: number }) =>
  instance.post<{ username: string; usertype: 0 | 1 }>('/signUp', data);
