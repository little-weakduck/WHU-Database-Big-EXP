<template>
  <div class="container">
    <div
      style="
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 100%;
      "
    >
      <div>
        <p>{{ course.type + ' ' + course.teacher + ' ' + course.credit + '学分' }}</p>
        <p>{{ course.capacity + '人 ' + course.time + ' ' + course.place }}</p>
      </div>
      <div>
        <el-button
          v-if="allowControl && !course.select && course.select !== undefined"
          type="primary"
          size="large"
          @click="handleClick"
          >选课</el-button
        >
        <el-button
          v-if="allowControl && course.select"
          type="danger"
          size="large"
          @click="handleClick"
          >退课</el-button
        >
      </div>
    </div>
    <el-divider direction="horizontal" content-position="left"></el-divider>
    <div style="width: 100%">
      <h2>评论</h2>
      <el-card
        v-for="(comment, index) in comments"
        :key="index"
        shadow="always"
        :body-style="{ padding: '20px' }"
        style="margin-bottom: 16px"
      >
        <template #header>
          <div
            style="
              display: flex;
              flex-direction: row;
              justify-content: space-between;
              align-items: center;
            "
          >
            <div style="display: flex; flex-direction: row; align-items: center; gap: 16px">
              <span>{{ comment.name }}</span>
              <el-rate
                v-model="comment.mark"
                :allow-half="true"
                disabled
                :colors="['#F56C6C', '#E6A23C', '#67C23A']"
              ></el-rate>
            </div>
            <span>{{ comment.time.toLocaleString() }}</span>
          </div>
        </template>
        <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
          <div>{{ comment.content }}</div>
          <el-button
            v-if="allowDeletePeople"
            style="align-self: flex-end"
            type="danger"
            size="default"
            @click=""
            >删除评论</el-button
          >
        </div>
      </el-card>
      <el-card
        v-if="allowControl"
        shadow="always"
        :body-style="{ padding: '20px' }"
        style="margin-bottom: 16px"
      >
        <template #header>
          <div
            style="
              display: flex;
              flex-direction: row;
              justify-content: space-between;
              align-items: center;
            "
          >
            <span>评论</span>
            <el-rate
              v-model="commentMark"
              :allow-half="true"
              :colors="['#F56C6C', '#E6A23C', '#67C23A']"
            ></el-rate>
          </div>
        </template>
        <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
          <el-input
            type="textarea"
            :rows="5"
            placeholder="请输入评论"
            v-model="commentContent"
          ></el-input>
          <el-button style="align-self: flex-end" type="primary" size="default" @click=""
            >评论</el-button
          >
        </div>
      </el-card>
      <div v-if="allowDeletePeople">
        <el-divider direction="horizontal" content-position="left"></el-divider>
        <h2>选课的人</h2>
        <el-table :data="selectPeople" style="width: 100%" stripe>
          <el-table-column prop="name" label="姓名" />
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button type="primary" size="small" @click.prevent="deletePeople(scope.row.name)">
                退课
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Course } from './CourseList.vue';
export interface Comment {
  name: string;
  content: string;
  time: Date;
  mark: number;
}
export interface SelectPeople {
  name: string;
}
const props = defineProps<{
  course: Course;
  allowControl: Boolean;
  allowDeletePeople?: boolean;
}>();

const course = props.course;

const comments = ref<Comment[]>([
  {
    name: '张三',
    content: '这门课很好',
    time: new Date(),
    mark: 2
  },
  {
    name: '李四',
    content: '这门课很好',
    time: new Date(),
    mark: 3.5
  },
  {
    name: '王五',
    content: '这门课很好',
    time: new Date(),
    mark: 5
  }
]);

const selectPeople = ref<SelectPeople[]>([
  {
    name: '张三'
  },
  {
    name: '李四'
  },
  {
    name: '王五'
  }
]);
const deletePeople = (name: string) => {
  console.log(name);
};

const commentContent = ref('');
const commentMark = ref(0);
</script>

<style scoped>
.container {
  display: flex;
  padding: 16px;
  flex-direction: column;
  justify-content: flex-start;
  gap: 0px;
}
</style>
