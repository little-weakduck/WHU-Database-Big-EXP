import type { Course } from '@/course/CourseList.vue';
import { instance, type ResponseBody } from './instance';

export interface CourseSelect {
  course: string;
  id: number;
  name: string;
}

export const joinCourse = (data: { username: string; coursename: string }) =>
  instance.post<ResponseBody<{}>>('/add', data);

export const dropCourse = (data: { username: string; coursename: string }) =>
  instance.post<ResponseBody<{}>>('/drop', data);

export const getAllCourse = () => instance.post<Course[]>('/course/all', {});
export const getSelectCourse = (data: { username: string }) =>
  instance.post<CourseSelect[]>('/show_already', data);

export const addCourse = (data: Course) => instance.post<ResponseBody<{}>>('/teacheradd', data);
export const changeCourse = (data: Course) => instance.post<{}>('/course/change', data);

export const getCourseStudent = (data: { coursename: string }) =>
  instance.post<CourseSelect[]>('/allstudent', data);
