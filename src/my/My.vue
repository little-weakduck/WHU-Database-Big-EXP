<template>
  <div class="ctn">
    <div style="display: flex; flex-direction: row; justify-content: space-between; width: 100%">
      <h1 style="padding-top: 0px; margin-top: 0px">
        {{ userType === '0' ? '已选的课' : '我上的课' }}
      </h1>
      <div>
        <el-button v-if="userType === '1'" type="primary" size="default" @click="startAddCourse"
          >添加课程</el-button
        >
      </div>
    </div>

    <div class="course">
      <el-card
        v-for="(course, index) in showCourseList"
        :key="index"
        shadow="hover"
        :body-style="{ padding: '20px', width: '300px' }"
        @click="clickCourse(course)"
      >
        <template #header>
          <div style="display: flex; flex-direction: row; justify-content: space-between">
            <span>{{ course.name }}</span>
            <div>
              <span>{{ course.credit }} 学分 </span>
              <span v-if="userType === '0'">{{ course.select ? '已选' : '未选' }}</span>
            </div>
          </div>
        </template>
        <div style="display: flex; gap: 4px; flex-direction: column">
          <div>授课教师：{{ course.teacher }}</div>
          <div>课程类型：{{ course.type }}</div>
          <div>上课时间：{{ course.time }}</div>
          <div>上课地点：{{ course.place }}</div>
          <div>课程容量：{{ course.capacity }}人</div>
        </div>
      </el-card>
      <h1 v-if="showCourseList.length === 0">
        {{ userType === '0' ? '还没有选课' : '还没有上的课' }}
      </h1>
      <div v-if="showCourseList.length % 3 !== 0" style="width: 340px" />
      <div v-if="showCourseList.length % 3 === 1" style="width: 340px" />
    </div>
  </div>
  <el-dialog v-model="showCourseDetail" destroy-on-close :title="detailCourse?.name" width="50%">
    <CourseDetail
      :course="detailCourse!"
      :allowControl="userType === '0'"
      :allowDeletePeople="userType === '1'"
      @changeStatus="handleChangeStatus"
    ></CourseDetail> </el-dialog
  ><el-dialog v-model="isShowAddCourse" title="添加课程" width="50%" append-to-body>
    <AddCourse />
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import CourseDetail from '../course/CourseDetail.vue';
import AddCourse from '@/course/AddCourse.vue';
import api from '@/api/api';

export interface Course {
  name: string;
  teacher: string;
  credit: number;
  type: string;
  time: string;
  place: string;
  capacity: number;
  select?: boolean;
}
const userType = localStorage.getItem('userType') || 0;
const userName = localStorage.getItem('userName') || '';

const clickCourse = (course: Course) => {
  detailCourse.value = course;
  console.log(
    '🚀 ~ file: CourseList.vue:55 ~ clickCourse ~   detailCourse.value:',
    detailCourse.value
  );
  showCourseDetail.value = true;
};

const courseList = ref<Course[]>([]);

const getCourse = () => {
  api.getAllCourse().then((res) => {
    courseList.value = res.data;
    if (userType === '0') {
      api.getSelectCourse({ username: userName! }).then((res) => {
        courseList.value = courseList.value.map((item) => {
          if (res.data.find((course) => course.course === item.name)) {
            return { ...item, select: true };
          } else return { ...item, select: false };
        });
      });
    }
  });
};
onMounted(() => {
  getCourse();
});

const handleChangeStatus = () => {
  getCourse();
};

const showCourseList = ref<Course[]>([]);

watch(courseList, (newVal) => {
  if (userType === '0') {
    showCourseList.value = newVal.filter((course) => course.select);
  } else {
    showCourseList.value = newVal.filter((course) => course.teacher === userName);
  }
});

// 添加课程
const isShowAddCourse = ref(false);
const startAddCourse = () => {
  isShowAddCourse.value = true;
};

// detail dialog
const showCourseDetail = ref(false);
const detailCourse = ref<Course>();
</script>

<style scoped>
.course {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 50px;
  width: 100%;
  align-items: flex-start;
}
.ctn {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 32px;
  padding: 16px;
}
</style>
