<template>
  <div class="app-container">
    <el-container style="height: 100vh;">
      <!-- 顶部导航栏 -->
      <el-header v-if="isLoggedIn" height="60px" class="header">
        <div class="header-left">
          <h1>校园疫情数据分析系统</h1>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              {{ user.name }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="navigateTo('/profile')">个人资料</el-dropdown-item>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 主体内容 -->
      <el-container>
        <!-- 左侧菜单 -->
        <el-aside v-if="isLoggedIn" width="200px" class="sidebar">
          <el-menu
            :default-active="activeMenu"
            class="sidebar-menu"
            router
          >
            <el-menu-item index="/home">
              <el-icon><home /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="/profile">
              <el-icon><user /></el-icon>
              <span>个人资料</span>
            </el-menu-item>
            
            <!-- 公共管理 -->
            <el-sub-menu v-if="user.role === 'admin'" index="public">
              <template #title>
                <el-icon><setting /></el-icon>
                <span>公共管理</span>
              </template>
              <el-menu-item index="/carousel">轮播图管理</el-menu-item>
              <el-menu-item index="/announcement">网站公告</el-menu-item>
            </el-sub-menu>
            
            <!-- 用户管理 -->
            <el-sub-menu v-if="user.role === 'admin'" index="user">
              <template #title>
                <el-icon><users /></el-icon>
                <span>用户管理</span>
              </template>
              <el-menu-item index="/users">用户列表</el-menu-item>
            </el-sub-menu>
            
            <!-- 信息管理 -->
            <el-sub-menu index="info">
              <template #title>
                <el-icon><document /></el-icon>
                <span>信息管理</span>
              </template>
              <el-menu-item index="/news">疫情资讯</el-menu-item>
              <el-menu-item v-if="user.role === 'admin'" index="/news-category">资讯分类</el-menu-item>
            </el-sub-menu>
            
            <!-- 疫情数据 -->
            <el-menu-item index="/covid-data">
              <el-icon><data-analysis /></el-icon>
              <span>疫情数据</span>
            </el-menu-item>
            
            <!-- 健康填报 -->
            <el-menu-item index="/health-report">
              <el-icon><monitor /></el-icon>
              <span>健康填报</span>
            </el-menu-item>
            
            <!-- 出入申请 -->
            <el-menu-item index="/entry-exit">
              <el-icon><position /></el-icon>
              <span>出入申请</span>
            </el-menu-item>
            
            <!-- 动态上报 -->
            <el-menu-item index="/dynamic-report">
              <el-icon><bell /></el-icon>
              <span>动态上报</span>
            </el-menu-item>
            
            <!-- 医务室管理 -->
            <el-sub-menu index="medical">
              <template #title>
                <el-icon><hospital /></el-icon>
                <span>医务室管理</span>
              </template>
              <el-menu-item index="/medical-office">医务室信息</el-menu-item>
              <el-menu-item index="/medical-assignment">医务室分配</el-menu-item>
            </el-sub-menu>
            
            <!-- 数据分析 -->
            <el-menu-item index="/analytics">
              <el-icon><pie-chart /></el-icon>
              <span>数据分析</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <!-- 主内容区 -->
        <el-main class="main-content">
          <router-view v-if="isLoggedIn" />
          <Login v-else />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Login from './components/Login.vue'
import { Home, User, Setting, Users, Document, DataAnalysis, Monitor, Position, Bell, Hospital, PieChart, ArrowDown } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    Login,
    Home,
    User,
    Setting,
    Users,
    Document,
    DataAnalysis,
    Monitor,
    Position,
    Bell,
    Hospital,
    PieChart,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    const user = ref({})
    
    const isLoggedIn = computed(() => {
      return localStorage.getItem('token') !== null
    })
    
    const activeMenu = computed(() => {
      return router.currentRoute.value.path
    })
    
    const navigateTo = (path) => {
      router.push(path)
    }
    
    const logout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }
    
    const loadUserInfo = () => {
      const userStr = localStorage.getItem('user')
      if (userStr) {
        user.value = JSON.parse(userStr)
      }
    }
    
    onMounted(() => {
      loadUserInfo()
    })
    
    return {
      user,
      isLoggedIn,
      activeMenu,
      navigateTo,
      logout
    }
  }
}
</script>

<style scoped>
.app-container {
  height: 100vh;
  overflow: hidden;
}

.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header h1 {
  margin: 0;
  font-size: 20px;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.sidebar {
  background-color: #f0f2f5;
  border-right: 1px solid #dcdfe6;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.main-content {
  padding: 20px;
  overflow-y: auto;
}
</style>