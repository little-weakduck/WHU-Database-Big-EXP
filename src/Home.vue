<template>
  <el-container>
    <el-header>
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        :ellipsis="false"
        router
      >
        <div class="name">
          {{ userName }}
        </div>
        <div class="flex-grow" />
        <el-menu-item index="course">课程</el-menu-item>
        <el-menu-item index="my">我的</el-menu-item>

        <div class="name">
          <el-popconfirm
            title="是否确定退出登录"
            confirm-button-text="确定"
            cancel-button-text="取消"
            hide-icon
            @confirm="logout"
          >
            <template #reference>
              <el-button>退出登录</el-button>
            </template>
          </el-popconfirm>
        </div>
      </el-menu>
    </el-header>
    <el-main>
      <CourseList v-if="route.name === 'Course'"></CourseList>
      <My v-if="route.name === 'My'"></My>
    </el-main>
  </el-container>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CourseList from './course/CourseList.vue';
import My from './my/My.vue';

const userName = localStorage.getItem('userName') || '';

const router = useRouter();
const route = useRoute();
const activeIndex = ref('1');
onMounted(() => {
  if (userName === '') {
    router.replace('/login');
  }
  if (route.name === 'Course') {
    activeIndex.value = 'course';
  }
  if (route.name === 'My') {
    activeIndex.value = 'my';
  }
});
const logout = () => {
  localStorage.clear();
  router.push('/login');
};
</script>

<style scoped>
.name {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 16px;
  font-size: large;
  font-weight: bold;
}
.flex-grow {
  flex-grow: 1;
}
</style>
