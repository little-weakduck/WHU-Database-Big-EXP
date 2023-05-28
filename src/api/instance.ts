import axios from 'axios';

export interface ResponseBody<T = any> {
  code: string;
  detail: string;
  msg: string;
  data: T;
}

export interface PageBody<T = any> {
  /**
   * 当页数量
   */
  count: number;
  /**
   * 下一页的接口
   */
  next: string | null;
  /**
   * 上一页的接口
   */
  previous: string | null;
  results: Array<T>;
}

export const instance = axios.create({
  baseURL: '/api',
  timeout: 30000
});

instance.interceptors.request.use(async (config) => {
  return config;
});
