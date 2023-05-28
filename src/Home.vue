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
        <div class="name">NAME</div>
        <div class="flex-grow" />
        <el-menu-item index="course">课程</el-menu-item>
        <el-menu-item index="my">我的</el-menu-item>
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

const router = useRouter();
const route = useRoute();
const activeIndex = ref('1');
onMounted(() => {
  if (route.name === 'Course') {
    activeIndex.value = 'course';
  }
  if (route.name === 'My') {
    activeIndex.value = 'my';
  }
});
</script>

<style scoped>
.name {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-left: 16px;
}
.flex-grow {
  flex-grow: 1;
}
</style>
