<template>
  <div class="medical-assignment-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>医务室分配</span>
          <el-button type="primary" @click="openAddDialog">提交申请</el-button>
        </div>
      </template>
      <el-table :data="assignments" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="medical_office_name" label="医务室" />
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
        <el-table-column prop="reason" label="申请原因" show-overflow-tooltip />
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
    <el-dialog v-model="dialogVisible" title="提交医务室申请">
      <el-form :model="assignmentForm" :rules="assignmentRules" ref="assignmentFormRef" label-width="100px">
        <el-form-item label="医务室" prop="medical_office_id">
          <el-select v-model="assignmentForm.medical_office_id">
            <el-option v-for="office in offices" :key="office.id" :label="office.name" :value="office.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="assignmentForm.start_time" type="datetime" placeholder="选择开始时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="assignmentForm.end_time" type="datetime" placeholder="选择结束时间" style="width: 100%" />
        </el-form-item>
        <el-form-item label="申请原因" prop="reason">
          <el-input v-model="assignmentForm.reason" type="textarea" :rows="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAssignment">提交</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'MedicalAssignment',
  setup() {
    const assignments = ref([])
    const offices = ref([])
    const dialogVisible = ref(false)
    const assignmentForm = ref({
      medical_office_id: '',
      start_time: '',
      end_time: '',
      reason: ''
    })
    const assignmentFormRef = ref(null)
    
    const assignmentRules = {
      medical_office_id: [
        { required: true, message: '请选择医务室', trigger: 'change' }
      ],
      start_time: [
        { required: true, message: '请选择开始时间', trigger: 'change' }
      ],
      end_time: [
        { required: true, message: '请选择结束时间', trigger: 'change' }
      ],
      reason: [
        { required: true, message: '请输入申请原因', trigger: 'blur' }
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
    
    const loadAssignments = async () => {
      try {
        const response = await axios.get('/api/medical-assignments')
        assignments.value = response.data
      } catch (error) {
        console.error('加载分配记录失败:', error)
      }
    }
    
    const loadOffices = async () => {
      try {
        const response = await axios.get('/api/medical-offices')
        offices.value = response.data
      } catch (error) {
        console.error('加载医务室信息失败:', error)
      }
    }
    
    const openAddDialog = () => {
      assignmentForm.value = {
        medical_office_id: '',
        start_time: '',
        end_time: '',
        reason: ''
      }
      dialogVisible.value = true
    }
    
    const submitAssignment = async () => {
      try {
        await assignmentFormRef.value.validate()
        // 格式化时间
        const formData = {
          ...assignmentForm.value,
          start_time: assignmentForm.value.start_time.toISOString().replace('T', ' ').substring(0, 19),
          end_time: assignmentForm.value.end_time.toISOString().replace('T', ' ').substring(0, 19)
        }
        await axios.post('/api/medical-assignments', formData)
        dialogVisible.value = false
        loadAssignments()
        alert('申请提交成功')
      } catch (error) {
        console.error('提交申请失败:', error)
        alert('提交失败，请重试')
      }
    }
    
    onMounted(() => {
      loadAssignments()
      loadOffices()
    })
    
    return {
      assignments,
      offices,
      dialogVisible,
      assignmentForm,
      assignmentFormRef,
      assignmentRules,
      formatDateTime,
      getStatusType,
      getStatusText,
      openAddDialog,
      submitAssignment
    }
  }
}
</script>

<style scoped>
.medical-assignment-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>