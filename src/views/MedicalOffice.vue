<template>
  <div class="medical-office-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>医务室信息管理</span>
          <el-button type="primary" @click="openAddDialog">添加医务室</el-button>
        </div>
      </template>
      <el-table :data="offices" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="医务室名称" />
        <el-table-column prop="location" label="位置" />
        <el-table-column prop="contact" label="联系方式" />
        <el-table-column prop="capacity" label="总容量" width="100" />
        <el-table-column prop="available" label="可用床位" width="100">
          <template #default="{ row }">
            <el-tag :type="row.available > 0 ? 'success' : 'danger'">{{ row.available }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteOffice(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑医务室对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="officeForm" :rules="officeRules" ref="officeFormRef" label-width="100px">
        <el-form-item label="医务室名称" prop="name">
          <el-input v-model="officeForm.name" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-input v-model="officeForm.location" />
        </el-form-item>
        <el-form-item label="联系方式" prop="contact">
          <el-input v-model="officeForm.contact" />
        </el-form-item>
        <el-form-item label="总容量" prop="capacity">
          <el-input-number v-model="officeForm.capacity" :min="1" />
        </el-form-item>
        <el-form-item label="可用床位" prop="available">
          <el-input-number v-model="officeForm.available" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveOffice">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'MedicalOffice',
  setup() {
    const offices = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加医务室')
    const officeForm = ref({
      name: '',
      location: '',
      contact: '',
      capacity: 1,
      available: 1
    })
    const officeFormRef = ref(null)
    const currentId = ref(null)
    
    const officeRules = {
      name: [
        { required: true, message: '请输入医务室名称', trigger: 'blur' }
      ],
      location: [
        { required: true, message: '请输入位置', trigger: 'blur' }
      ],
      contact: [
        { required: true, message: '请输入联系方式', trigger: 'blur' }
      ],
      capacity: [
        { required: true, message: '请输入总容量', trigger: 'blur' }
      ],
      available: [
        { required: true, message: '请输入可用床位', trigger: 'blur' }
      ]
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
      dialogTitle.value = '添加医务室'
      officeForm.value = {
        name: '',
        location: '',
        contact: '',
        capacity: 1,
        available: 1
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑医务室'
      officeForm.value = { ...row }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveOffice = async () => {
      try {
        await officeFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/medical-offices/${currentId.value}`, officeForm.value)
        } else {
          // 添加
          await axios.post('/api/medical-offices', officeForm.value)
        }
        dialogVisible.value = false
        loadOffices()
        alert('保存成功')
      } catch (error) {
        console.error('保存医务室信息失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteOffice = async (id) => {
      if (confirm('确定要删除这个医务室吗？')) {
        try {
          await axios.delete(`/api/medical-offices/${id}`)
          loadOffices()
          alert('删除成功')
        } catch (error) {
          console.error('删除医务室失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadOffices()
    })
    
    return {
      offices,
      dialogVisible,
      dialogTitle,
      officeForm,
      officeFormRef,
      officeRules,
      openAddDialog,
      openEditDialog,
      saveOffice,
      deleteOffice
    }
  }
}
</script>

<style scoped>
.medical-office-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>