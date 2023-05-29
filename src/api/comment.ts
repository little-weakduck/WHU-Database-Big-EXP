import { instance, type ResponseBody } from './instance';

export interface Comment {
  id?: number;
  comment: string;
  name: string;
  coursename: string;
  comment_time: Date;
  rank: number;
}

export const comment = (data: Comment) => instance.post<ResponseBody<{}>>('/comment', data);

export const delComment = (data: { commentid: number }) =>
  instance.post<ResponseBody<{}>>('/delcom', data);

export const getComment = (data: { coursename: string }) =>
  instance.post<Comment[]>('/showcoment', data);
