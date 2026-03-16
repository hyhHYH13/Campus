<template>
  <div class="dynamic-report-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>动态上报</span>
          <el-button type="primary" @click="openAddDialog">提交动态</el-button>
        </div>
      </template>
      <el-table :data="reports" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="content" label="动态内容" show-overflow-tooltip />
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="created_at" label="上报时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 提交动态对话框 -->
    <el-dialog v-model="dialogVisible" title="提交动态">
      <el-form :model="reportForm" :rules="reportRules" ref="reportFormRef" label-width="100px">
        <el-form-item label="动态内容" prop="content">
          <el-input v-model="reportForm.content" type="textarea" :rows="5" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="reportForm.location" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitReport">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'DynamicReport',
  setup() {
    const reports = ref([])
    const dialogVisible = ref(false)
    const reportForm = ref({
      content: '',
      location: ''
    })
    const reportFormRef = ref(null)
    
    const reportRules = {
      content: [
        { required: true, message: '请输入动态内容', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入位置', trigger: 'blur' }
      ]
    }
    
    const formatDateTime = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const loadReports = async () => {
      try {
        const response = await axios.get('/api/dynamic-reports')
        reports.value = response.data
      } catch (error) {
        console.error('加载动态记录失败:', error)
      }
    }
    
    const openAddDialog = () => {
      reportForm.value = {
        content: '',
        location: ''
      }
      dialogVisible.value = true
    }
    
    const submitReport = async () => {
      try {
        await reportFormRef.value.validate()
        await axios.post('/api/dynamic-reports', reportForm.value)
        dialogVisible.value = false
        loadReports()
        alert('动态提交成功')
      } catch (error) {
        console.error('提交动态失败:', error)
        alert('提交失败，请重试')
      }
    }
    
    onMounted(() => {
      loadReports()
    })
    
    return {
      reports,
      dialogVisible,
      reportForm,
      reportFormRef,
      reportRules,
      formatDateTime,
      openAddDialog,
      submitReport
    }
  }
}
</script>

<style scoped>
.dynamic-report-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>