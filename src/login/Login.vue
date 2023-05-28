<template>
  <el-container style="min-height: 100vh; min-width: 100vw">
    <el-aside width="45%" class="aside" style="">
      <img :src="currentBg" alt="" style="width: 100%; max-width: 600px; max-height: 600px" />
    </el-aside>
    <el-main class="main">
      <el-space direction="vertical" fill style="width: 400px" size="large">
        <div>
          <h1 style="font-size: 32px; text-align: center; margin-bottom: 12px; font-weight: 500">
            tmd想个名字啊
          </h1>
          <h2 style="font-size: 16px; color: #aaa; text-align: center; font-weight: normal">
            {{ route.name === 'Login' ? '账号登录' : '注册帐号' }}
          </h2>
        </div>
        <el-form
          v-if="route.name === 'Login'"
          ref="loginFormRef"
          label-position="top"
          :model="loginFormModel"
          :rules="loginRules"
        >
          <el-form-item label="账号" prop="username">
            <el-input
              v-model="loginFormModel.username"
              placeholder="请输入账号"
              :prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="loginFormModel.password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              type="password"
              show-password
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="flex: 1" :loading="loading" @click="login"
              >登录</el-button
            ><el-button type="info" style="flex: 1" :loading="loading" @click="toRegister"
              >前往注册</el-button
            >
          </el-form-item>
        </el-form>
        <el-form
          v-else
          ref="registerFormRef"
          label-position="right"
          :model="registerFormModel"
          :rules="registerRules"
        >
          <el-form-item label="账号" prop="username">
            <el-input
              v-model="registerFormModel.username"
              placeholder="请输入账号"
              :prefix-icon="User"
            />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerFormModel.password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              type="password"
              show-password
            /> </el-form-item
          ><el-form-item label="身份" prop="type">
            <el-select v-model="registerFormModel.type" class="m-2" placeholder="请选择身份">
              <el-option key="0" label="学生" :value="0" />
              <el-option key="1" label="老师" :value="1" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="info" style="flex: 1" :loading="loading" @click="toLogin"
              >返回登录</el-button
            ><el-button type="primary" style="flex: 1" :loading="loading" @click="register"
              >注册</el-button
            >
          </el-form-item>
        </el-form>
      </el-space>
      <div class="footer">
        <p class="copyright">武汉大学国家网络安全学院xxx出品</p>
      </div>
    </el-main>
  </el-container>
  <dark-switch style="position: absolute; top: 20px; right: 30px" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, FormInstance, FormRules } from 'element-plus';
import api from '../api/api';

const router = useRouter();
const route = useRoute();

const currentBg = ['/login/bg1.svg', '/login/bg2.svg', '/login/bg3.svg'][
  Math.floor(Math.random() * 3)
];

const loading = ref(false);

const loginFormRef = ref<FormInstance>();
const registerFormRef = ref<FormInstance>();
const loginFormModel = ref<{
  username: string;
  password: string;
}>({
  username: '',
  password: ''
});
const loginRules: FormRules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
};

const login = async () => {
  if (!loginFormRef.value) return;
  try {
    await loginFormRef.value.validate();
  } catch (err) {
    return;
  }
  try {
    const loginRes = await api.login({
      username: loginFormModel.value.username,
      password: loginFormModel.value.password
    });

    localStorage.setItem('userName', loginRes.data.name);
    localStorage.setItem('userType', loginRes.data.usertype);
    ElMessage.success('登陆成功！');
    router.replace('/course');
  } catch (err) {
    ElMessage.error('登录失败！请检查账号密码是否正确！');
  }
};
const register = async () => {
  if (!registerFormRef.value) return;
  try {
    await registerFormRef.value.validate();
  } catch (err) {
    return;
  }
  try {
    const registerRes = await api.register({
      username: registerFormModel.value.username,
      password: registerFormModel.value.password,
      usertype: registerFormModel.value.type
    });
    console.log(registerRes);

    localStorage.setItem('userName', registerRes.data.username);
    localStorage.setItem('userType', registerRes.data.usertype);
    ElMessage.success('注册成功！');
    router.replace('/course');
  } catch (err) {
    ElMessage.error('登录失败！请检查账号密码是否正确！');
  }
};

const toRegister = () => {
  router.push('/register');
};
const toLogin = () => {
  router.push('/login');
};

const registerFormModel = ref<{
  username: string;
  password: string;
  type: 0 | 1;
}>({
  username: '',
  password: '',
  type: 0
});
const registerRules: FormRules = {
  username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  type: [{ required: true, message: '请选择身份', trigger: 'blur' }]
};
</script>

<style lang="less" scoped>
* {
  box-sizing: border-box;
}

.form {
  width: 100%;
  max-width: 400px;
}

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 10px 4px rgba(0, 0, 0, 0.02);
}

.aside {
  display: flex;
  background: #f5f5f5;
  justify-content: center;
  align-items: center;

  @media (max-width: 768px) {
    display: none;
  }
}

.dark .aside {
  background: #272727;
}

.footer {
  position: absolute;
  bottom: 20px;
  font-size: 12px;
  color: #606266;
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 12px;

  .copyright {
    @media (max-height: 450px) {
      & {
        display: none;
      }
    }
  }

  .divider {
    height: 12px;
    width: 0;
    border-left: 1px solid #aaa;
  }

  a {
    transition: color 0.3s;
    cursor: pointer;

    &:hover {
      color: var(--el-color-primary);
    }
  }
}

.dark .footer {
  color: #ccc;
}
</style>
