<template>
  <div class="health-report-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>健康填报</span>
        </div>
      </template>
      <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef" label-width="100px">
        <el-form-item label="体温" prop="temperature">
          <el-input-number v-model="reportForm.temperature" :min="35" :max="42" :step="0.1" :precision="1" />
        </el-form-item>
        <el-form-item label="症状" prop="symptoms">
          <el-input v-model="reportForm.symptoms" type="textarea" placeholder="请输入症状，如无请填写'无'" />
        </el-form-item>
        <el-form-item label="当前位置" prop="location">
          <el-input v-model="reportForm.location" />
        </el-form-item>
        <el-form-item label="健康状态" prop="health_status">
          <el-radio-group v-model="reportForm.health_status">
            <el-radio label="healthy">健康</el-radio>
            <el-radio label="abnormal">异常</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitReport">提交填报</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 历史填报记录 -->
    <el-card class="mt-20">
      <template #header>
        <div class="card-header">
          <span>历史填报记录</span>
        </div>
      </template>
      <el-table :data="historyReports" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="temperature" label="体温" width="100" />
        <el-table-column prop="symptoms" label="症状" show-overflow-tooltip />
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="health_status" label="健康状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.health_status === 'healthy' ? 'success' : 'danger'">
              {{ row.health_status === 'healthy' ? '健康' : '异常' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="填报时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'HealthReport',
  setup() {
    const reportForm = ref({
      temperature: 36.5,
      symptoms: '无',
      location: '',
      health_status: 'healthy'
    })
    const reportFormRef = ref(null)
    const historyReports = ref([])
    
    const reportRules = {
      temperature: [
        { required: true, message: '请输入体温', trigger: 'blur' }
      ],
      symptoms: [
        { required: true, message: '请输入症状', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入当前位置', trigger: 'blur' }
      ],
      health_status: [
        { required: true, message: '请选择健康状态', trigger: 'change' }
      ]
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const loadHistoryReports = async () => {
      try {
        const response = await axios.get('/api/health-reports')
        historyReports.value = response.data
      } catch (error) {
        console.error('加载历史记录失败:', error)
      }
    }
    
    const submitReport = async () => {
      try {
        await reportFormRef.value.validate()
        await axios.post('/api/health-reports', reportForm.value)
        alert('填报成功')
        // 重置表单
        reportForm.value = {
          temperature: 36.5,
          symptoms: '无',
          location: '',
          health_status: 'healthy'
        }
        // 重新加载历史记录
        loadHistoryReports()
      } catch (error) {
        console.error('提交填报失败:', error)
        alert('提交失败，请重试')
      }
    }
    
    onMounted(() => {
      loadHistoryReports()
    })
    
    return {
      reportForm,
      reportFormRef,
      reportRules,
      historyReports,
      formatDate,
      submitReport
    }
  }
}
</script>

<style scoped>
.health-report-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mt-20 {
  margin-top: 20px;
}
</style>