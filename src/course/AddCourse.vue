<template>
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
  <div style="display: flex; flex-direction: row; justify-content: flex-end; align-items: center">
    <el-button v-if="!course" type="primary" @click="addCourse">立即创建</el-button>
    <el-button v-else type="primary" @click="changeCourse">修改</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { FormRules, FormInstance, ElMessage } from 'element-plus';
import api from '@/api/api';
import type { Course } from './CourseList.vue';

const props = defineProps<{ course?: Course }>();

const addCourseFormModel = ref<{
  name: string;
  credit: number;
  type: string;
  time: string;
  place: string;
  capacity: number;
}>({
  name: props.course?.name || '',
  credit: props.course?.credit || 0,
  type: props.course?.type || '',
  time: props.course?.time || '',
  place: props.course?.place || '',
  capacity: props.course?.capacity || 0
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

const userName = localStorage.getItem('userName') || '';

const emits = defineEmits(['change']);

const addCourse = async () => {
  if (!addCourseFormRef.value) return;
  try {
    await addCourseFormRef.value.validate();
  } catch (err) {
    return;
  }
  try {
    api.addCourse({ ...addCourseFormModel.value, teacher: userName });
    ElMessage.success('添加成功');
    emits('change');
  } catch {
    ElMessage.error('出错了');
  }
};
const changeCourse = async () => {
  if (!addCourseFormRef.value) return;
  try {
    await addCourseFormRef.value.validate();
  } catch (err) {
    return;
  }
  try {
    api.changeCourse({ ...addCourseFormModel.value, teacher: userName });
    ElMessage.success('修改成功');
    emits('change');
  } catch {
    ElMessage.error('出错了');
  }
};
</script>
