<template>
  <div class="entry-exit-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>出入申请</span>
          <el-button type="primary" @click="openAddDialog">提交申请</el-button>
        </div>
      </template>
      <el-table :data="applications" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="purpose" label="申请目的" />
        <el-table-column prop="start_time" label="开始时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="destination" label="目的地" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 提交申请对话框 -->
    <el-dialog v-model="dialogVisible" title="提交出入申请">
      <el-form :model="applicationForm" :rules="applicationRules" ref="applicationFormRef" label-width="100px">
        <el-form-item label="申请目的" prop="purpose">
          <el-input v-model="applicationForm.purpose" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="applicationForm.start_time" type="datetime" placeholder="选择开始时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="applicationForm.end_time" type="datetime" placeholder="选择结束时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="目的地" prop="destination">
          <el-input v-model="applicationForm.destination" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitApplication">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'EntryExit',
  setup() {
    const applications = ref([])
    const dialogVisible = ref(false)
    const applicationForm = ref({
      purpose: '',
      start_time: '',
      end_time: '',
      destination: ''
    })
    const applicationFormRef = ref(null)
    
    const applicationRules = {
      purpose: [
        { required: true, message: '请输入申请目的', trigger: 'blur' }
      ],
      start_time: [
        { required: true, message: '请选择开始时间', trigger: 'change' }
      ],
      end_time: [
        { required: true, message: '请选择结束时间', trigger: 'change' }
      ],
      destination: [
        { required: true, message: '请输入目的地', trigger: 'blur' }
      ]
    }
    
    const formatDateTime = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const getStatusType = (status) => {
      switch (status) {
        case 'pending': return 'warning'
        case 'approved': return 'success'
        case 'rejected': return 'danger'
        default: return ''
      }
    }
    
    const getStatusText = (status) => {
      switch (status) {
        case 'pending': return '待审核'
        case 'approved': return '已批准'
        case 'rejected': return '已拒绝'
        default: return status
      }
    }
    
    const loadApplications = async () => {
      try {
        const response = await axios.get('/api/entry-exit')
        applications.value = response.data
      } catch (error) {
        console.error('加载申请记录失败:', error)
      }
    }
    
    const openAddDialog = () => {
      applicationForm.value = {
        purpose: '',
        start_time: '',
        end_time: '',
        destination: ''
      }
      dialogVisible.value = true
    }
    
    const submitApplication = async () => {
      try {
        await applicationFormRef.value.validate()
        // 格式化时间
        const formData = {
          ...applicationForm.value,
          start_time: applicationForm.value.start_time.toISOString().replace('T', ' ').substring(0, 19),
          end_time: applicationForm.value.end_time.toISOString().replace('T', ' ').substring(0, 19)
        }
        await axios.post('/api/entry-exit', formData)
        dialogVisible.value = false
        loadApplications()
        alert('申请提交成功')
      } catch (error) {
        console.error('提交申请失败:', error)
        alert('提交失败，请重试')
      }
    }
    
    onMounted(() => {
      loadApplications()
    })
    
    return {
      applications,
      dialogVisible,
      applicationForm,
      applicationFormRef,
      applicationRules,
      formatDateTime,
      getStatusType,
      getStatusText,
      openAddDialog,
      submitApplication
    }
  }
}
</script>

<style scoped>
.entry-exit-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>