<template>
  <div class="ctn">
    <el-checkbox-group v-model="type">
      <el-checkbox-button v-for="typeItem in types" :key="typeItem" :label="typeItem">{{
        typeItem
      }}</el-checkbox-button>
    </el-checkbox-group>

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
              <span v-if="course.select !== undefined">{{ course.select ? '已选' : '未选' }}</span>
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
      <div v-if="showCourseList.length % 3 !== 0" style="width: 340px" />
      <div v-if="showCourseList.length % 3 === 1" style="width: 340px" />
    </div>
  </div>
  <el-dialog v-model="showCourseDetail" :title="detailCourse?.name" width="50%">
    <CourseDetail :course="detailCourse!" :allowControl="userType === '0'"></CourseDetail>
  </el-dialog>
</template>

<script setup lang="ts">
import router from '@/router';
import { ref, watch } from 'vue';
import CourseDetail from './CourseDetail.vue';

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

const type = ref(['公共必修课', '公共选修课', '专业必修课', '专业选修课']);
const types = ref(['公共必修课', '公共选修课', '专业必修课', '专业选修课']);

const clickCourse = (course: Course) => {
  detailCourse.value = course;
  console.log(
    '🚀 ~ file: CourseList.vue:55 ~ clickCourse ~   detailCourse.value:',
    detailCourse.value
  );
  showCourseDetail.value = true;
};
const courseList = ref<Course[]>([
  {
    name: '计算机网络',
    teacher: '张三',
    credit: 3,
    type: '公共必修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: true
  },
  {
    name: '速度速度上',
    teacher: '张三',
    credit: 3,
    type: '公共选修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: true
  },
  {
    name: '说的是',
    teacher: '张三',
    credit: 3,
    type: '专业必修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100
  },
  {
    name: '高铁热热',
    teacher: '张三',
    credit: 3,
    type: '专业必修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: true
  },
  {
    name: '好讨厌你',
    teacher: '张三',
    credit: 3,
    type: '专业选修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: false
  },
  {
    name: '具有头发改变',
    teacher: '张三',
    credit: 3,
    type: '专业选修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: false
  },
  {
    name: '通过人工',
    teacher: '张三',
    credit: 3,
    type: '专业选修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: false
  },
  {
    name: '投入更多的',
    teacher: '张三',
    credit: 3,
    type: '公共必修课',
    time: '周一 1-2节',
    place: '教学楼A101',
    capacity: 100,
    select: false
  }
]);
watch([type, courseList], (newVal) => {
  showCourseList.value = courseList.value.filter((item) => newVal[0].includes(item.type));
});
const showCourseList = ref<Course[]>([]);
showCourseList.value = courseList.value;

const userType = localStorage.getItem('userType');

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
