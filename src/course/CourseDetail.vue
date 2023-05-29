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
          v-if="allowControl && !course.select"
          type="primary"
          size="large"
          @click="joinCourse"
          >选课</el-button
        >
        <el-button
          v-if="allowControl && course.select"
          type="danger"
          size="large"
          @click="dropCourse"
          >退课</el-button
        >
        <el-button v-if="allowDeletePeople" type="primary" size="large" @click="startChangeCourse"
          >修改</el-button
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
                v-model="comment.rank"
                :allow-half="true"
                disabled
                :colors="['#F56C6C', '#E6A23C', '#67C23A']"
              ></el-rate>
            </div>
            <span>{{ comment.comment_time.toLocaleString() }}</span>
          </div>
        </template>
        <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
          <div>{{ comment.comment }}</div>
          <el-button
            v-if="allowDeletePeople || comment.name === userName"
            style="align-self: flex-end"
            type="danger"
            size="default"
            @click="deleteComment(comment.id!)"
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
          <el-button style="align-self: flex-end" type="primary" size="default" @click="addComment"
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
  <el-dialog title="修改课程信息" v-model="isShowChangeCourse" width="50%">
    <AddCourse :course="course" @change="isShowChangeCourse = !isShowChangeCourse" />
  </el-dialog>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Course } from './CourseList.vue';
import api from '@/api/api';
import { type Comment } from '@/api/comment';
import { type CourseSelect } from '@/api/course';
import { ElMessage } from 'element-plus';
import AddCourse from './AddCourse.vue';

const props = defineProps<{
  course: Course;
  allowControl: Boolean;
  allowDeletePeople?: boolean;
}>();

const emits = defineEmits(['changeStatus']);

const course = ref(props.course);
const userName = localStorage.getItem('userName');

const joinCourse = () => {
  api.joinCourse({ username: userName!, coursename: course.value.name }).then(() => {
    course.value.select = true;
    emits('changeStatus');
  });
};
const dropCourse = () => {
  api.dropCourse({ username: userName!, coursename: course.value.name }).then(() => {
    course.value.select = false;
    emits('changeStatus');
  });
};

const isShowChangeCourse = ref(false);
const startChangeCourse = () => {
  isShowChangeCourse.value = true;
};

onMounted(() => {
  getComment();
  if (props.allowDeletePeople) {
    getCourseStudent();
  }
});

const getCourseStudent = () => {
  api.getCourseStudent({ coursename: course.value.name }).then((res) => {
    selectPeople.value = res.data;
  });
};

const getComment = () => {
  api.getComment({ coursename: course.value.name }).then((res) => {
    comments.value = res.data.map((comment) => {
      return {
        ...comment,
        comment_time: new Date(comment.comment_time)
      };
    });
  });
};

const comments = ref<Comment[]>([]);

const selectPeople = ref<CourseSelect[]>([]);
const deletePeople = (name: string) => {
  api.dropCourse({ username: name, coursename: course.value.name }).then(() => {
    getCourseStudent();
  });
};

const commentContent = ref('');
const commentMark = ref(0);
const addComment = () => {
  if (commentContent.value === '' || commentMark.value === 0) {
    ElMessage.error('评论内容和评分不能为空');
  }
  api
    .comment({
      name: userName!,
      coursename: course.value.name,
      comment: commentContent.value,
      rank: commentMark.value,
      comment_time: new Date()
    })
    .then(() => {
      commentContent.value = '';
      commentMark.value = 0;
      getComment();
    });
};

const deleteComment = (comment_id: number) => {
  api.delComment({ commentid: comment_id }).then(() => {
    getComment();
  });
};
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
