<template>
  <div class="home-container">
    <!-- 轮播图 -->
    <el-carousel :interval="5000" type="card" height="400px">
      <el-carousel-item v-for="carousel in carousels" :key="carousel.id">
        <img :src="carousel.image_url" :alt="carousel.title" style="width: 100%; height: 100%; object-fit: cover;" />
        <div class="carousel-caption">
          <h3>{{ carousel.title }}</h3>
        </div>
      </el-carousel-item>
    </el-carousel>
    
    <!-- 数据概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <el-icon class="stat-icon"><data-analysis /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ covidData?.confirmed || 0 }}</div>
              <div class="stat-label">确诊病例</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <el-icon class="stat-icon"><success /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ covidData?.recovered || 0 }}</div>
              <div class="stat-label">康复病例</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <el-icon class="stat-icon"><monitor /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ healthStats?.healthy || 0 }}</div>
              <div class="stat-label">健康人数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <el-icon class="stat-icon"><warning /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ healthStats?.abnormal || 0 }}</div>
              <div class="stat-label">异常人数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最新公告 -->
    <el-card class="announcement-card">
      <template #header>
        <div class="card-header">
          <span>最新公告</span>
          <el-button type="primary" size="small" @click="navigateTo('/announcement')" v-if="user.role === 'admin'">管理公告</el-button>
        </div>
      </template>
      <el-timeline>
        <el-timeline-item
          v-for="announcement in announcements"
          :key="announcement.id"
          :timestamp="formatDate(announcement.created_at)"
        >
          <el-card>
            <h3>{{ announcement.title }}</h3>
            <p>{{ announcement.content.substring(0, 100) }}...</p>
            <div class="announcement-meta">
              <span>发布人: {{ announcement.author }}</span>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
    
    <!-- 最新资讯 -->
    <el-card class="news-card">
      <template #header>
        <div class="card-header">
          <span>最新资讯</span>
          <el-button type="primary" size="small" @click="navigateTo('/news')" v-if="user.role === 'admin'">管理资讯</el-button>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8" v-for="news in latestNews" :key="news.id">
          <el-card shadow="hover">
            <img v-if="news.image_url" :src="news.image_url" :alt="news.title" style="width: 100%; height: 150px; object-fit: cover; margin-bottom: 10px;" />
            <h3>{{ news.title }}</h3>
            <p>{{ news.content.substring(0, 80) }}...</p>
            <div class="news-meta">
              <span>{{ news.category_name }}</span>
              <span>{{ formatDate(news.created_at) }}</span>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { DataAnalysis, Success, Monitor, Warning } from '@element-plus/icons-vue'

export default {
  name: 'Home',
  components: {
    DataAnalysis,
    Success,
    Monitor,
    Warning
  },
  setup() {
    const router = useRouter()
    const carousels = ref([])
    const announcements = ref([])
    const latestNews = ref([])
    const covidData = ref(null)
    const healthStats = ref(null)
    const user = ref(JSON.parse(localStorage.getItem('user')))
    
    const navigateTo = (path) => {
      router.push(path)
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
    }
    
    const loadCarousels = async () => {
      try {
        const response = await axios.get('/api/carousels')
        carousels.value = response.data
      } catch (error) {
        console.error('加载轮播图失败:', error)
      }
    }
    
    const loadAnnouncements = async () => {
      try {
        const response = await axios.get('/api/announcements')
        announcements.value = response.data.slice(0, 5)
      } catch (error) {
        console.error('加载公告失败:', error)
      }
    }
    
    const loadLatestNews = async () => {
      try {
        const response = await axios.get('/api/news')
        latestNews.value = response.data.slice(0, 3)
      } catch (error) {
        console.error('加载资讯失败:', error)
      }
    }
    
    const loadCovidData = async () => {
      try {
        const response = await axios.get('/api/covid-data')
        if (response.data.length > 0) {
          covidData.value = response.data[0]
        }
      } catch (error) {
        console.error('加载疫情数据失败:', error)
      }
    }
    
    const loadHealthStats = async () => {
      try {
        const response = await axios.get('/api/analytics/health-status')
        healthStats.value = response.data
      } catch (error) {
        console.error('加载健康状态数据失败:', error)
      }
    }
    
    onMounted(() => {
      loadCarousels()
      loadAnnouncements()
      loadLatestNews()
      loadCovidData()
      loadHealthStats()
    })
    
    return {
      carousels,
      announcements,
      latestNews,
      covidData,
      healthStats,
      user,
      navigateTo,
      formatDate
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px 0;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 20px;
}

.carousel-caption h3 {
  margin: 0;
}

.stats-row {
  margin: 30px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  font-size: 48px;
  color: #409EFF;
  margin-right: 20px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 16px;
  color: #909399;
  margin-top: 5px;
}

.announcement-card,
.news-card {
  margin-top: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.announcement-meta {
  margin-top: 10px;
  font-size: 14px;
  color: #909399;
}

.news-meta {
  margin-top: 10px;
  font-size: 14px;
  color: #909399;
  display: flex;
  justify-content: space-between;
}
</style>