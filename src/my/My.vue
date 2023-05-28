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
      <div v-if="showCourseList.length % 3 !== 0" style="width: 340px" />
      <div v-if="showCourseList.length % 3 === 1" style="width: 340px" />
    </div>
  </div>
  <el-dialog v-model="showCourseDetail" :title="detailCourse?.name" width="50%">
    <CourseDetail
      :course="detailCourse!"
      :allowControl="userType === '0'"
      :allowDeletePeople="userType === '1'"
    ></CourseDetail> </el-dialog
  ><el-dialog v-model="isShowAddCourse" title="添加课程" width="50%">
    <el-form
      ref="addCourseFormRef"
      :model="addCourseFormModel"
      :rules="addCourseRules"
      label-position="left"
      label-width="80px"
    >
      <el-form-item label="课程名" prop="name">
        <el-input v-model="addCourseFormModel.name"></el-input>
      </el-form-item>
      <el-form-item label="课程类型" prop="type">
        <el-select v-model="addCourseFormModel.type" placeholder="请选择课程类型">
          <el-option label="公共必修课" value="公共必修课"> </el-option>
          <el-option label="公共选修课" value="公共选修课"> </el-option>
          <el-option label="专业必修课" value="专业必修课"> </el-option>
          <el-option label="专业选修课" value="专业选修课"> </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="学分" prop="credit">
        <el-input-number v-model="addCourseFormModel.credit" :min="1" />
      </el-form-item>
      <el-form-item label="上课时间" prop="time">
        <el-input v-model="addCourseFormModel.time"></el-input>
      </el-form-item>
      <el-form-item label="上课地点" prop="place">
        <el-input v-model="addCourseFormModel.place"></el-input>
      </el-form-item>
      <el-form-item label="课程容量" prop="capacity">
        <el-input-number v-model="addCourseFormModel.capacity" :min="1" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button>取消</el-button>
      <el-button type="primary" @click="addCourse">立即创建</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import router from '@/router';
import { onMounted, ref, watch } from 'vue';
import CourseDetail from '../course/CourseDetail.vue';
import { FormRules, FormInstance } from 'element-plus';

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

onMounted(() => {
  setTimeout(() => {
    courseList.value = [
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
        teacher: '张',
        credit: 3,
        type: '专业选修课',
        time: '周一 1-2节',
        place: '教学楼A101',
        capacity: 100,
        select: false
      },
      {
        name: '投入更多的',
        teacher: '张',
        credit: 3,
        type: '公共必修课',
        time: '周一 1-2节',
        place: '教学楼A101',
        capacity: 100,
        select: false
      }
    ];
  }, 300);
});

const showCourseList = ref<Course[]>([]);
localStorage.setItem('userType', '1');
localStorage.setItem('userName', '张');

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
const addCourseFormModel = ref<{
  name: string;
  credit: number;
  type: string;
  time: string;
  place: string;
  capacity: number;
}>({
  name: '',
  credit: 1,
  type: '',
  time: '',
  place: '',
  capacity: 1
});
const addCourseRules: FormRules = {
  name: [{ required: true, message: '请输入课程名称', trigger: 'blur' }],
  credit: [{ required: true, message: '请输入学分', trigger: 'blur' }],
  type: [{ required: true, message: '请选择课程类型', trigger: 'blur' }],
  time: [{ required: true, message: '请输入上课时间', trigger: 'blur' }],
  place: [{ required: true, message: '请输入上课时间', trigger: 'blur' }],
  capacity: [{ required: true, message: '请输入课程容量', trigger: 'blur' }]
};
const addCourseFormRef = ref<FormInstance>();

const addCourse = async () => {
  if (!addCourseFormRef.value) return;
  try {
    await addCourseFormRef.value.validate();
  } catch (err) {
    return;
  }
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
