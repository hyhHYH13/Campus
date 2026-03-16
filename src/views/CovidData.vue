<template>
  <div class="covid-data-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>疫情数据管理</span>
          <el-button type="primary" @click="openAddDialog">添加数据</el-button>
        </div>
      </template>
      <el-table :data="covidData" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="confirmed" label="确诊病例" width="100" />
        <el-table-column prop="suspected" label="疑似病例" width="100" />
        <el-table-column prop="recovered" label="康复病例" width="100" />
        <el-table-column prop="deaths" label="死亡病例" width="100" />
        <el-table-column prop="campus_area" label="校区" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteData(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑数据对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="dataForm" :rules="dataRules" ref="dataFormRef" label-width="100px">
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="dataForm.date" type="date" placeholder="选择日期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="确诊病例" prop="confirmed">
          <el-input-number v-model="dataForm.confirmed" :min="0" />
        </el-form-item>
        <el-form-item label="疑似病例" prop="suspected">
          <el-input-number v-model="dataForm.suspected" :min="0" />
        </el-form-item>
        <el-form-item label="康复病例" prop="recovered">
          <el-input-number v-model="dataForm.recovered" :min="0" />
        </el-form-item>
        <el-form-item label="死亡病例" prop="deaths">
          <el-input-number v-model="dataForm.deaths" :min="0" />
        </el-form-item>
        <el-form-item label="校区" prop="campus_area">
          <el-input v-model="dataForm.campus_area" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveData">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'CovidData',
  setup() {
    const covidData = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加疫情数据')
    const dataForm = ref({
      date: '',
      confirmed: 0,
      suspected: 0,
      recovered: 0,
      deaths: 0,
      campus_area: ''
    })
    const dataFormRef = ref(null)
    const currentId = ref(null)
    
    const dataRules = {
      date: [
        { required: true, message: '请选择日期', trigger: 'change' }
      ],
      confirmed: [
        { required: true, message: '请输入确诊病例数', trigger: 'blur' }
      ],
      suspected: [
        { required: true, message: '请输入疑似病例数', trigger: 'blur' }
      ],
      recovered: [
        { required: true, message: '请输入康复病例数', trigger: 'blur' }
      ],
      deaths: [
        { required: true, message: '请输入死亡病例数', trigger: 'blur' }
      ],
      campus_area: [
        { required: true, message: '请输入校区', trigger: 'blur' }
      ]
    }
    
    const loadCovidData = async () => {
      try {
        const response = await axios.get('/api/covid-data')
        covidData.value = response.data
      } catch (error) {
        console.error('加载疫情数据失败:', error)
      }
    }
    
    const openAddDialog = () => {
      dialogTitle.value = '添加疫情数据'
      dataForm.value = {
        date: '',
        confirmed: 0,
        suspected: 0,
        recovered: 0,
        deaths: 0,
        campus_area: ''
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑疫情数据'
      // 处理日期格式
      const date = new Date(row.date)
      dataForm.value = {
        ...row,
        date: date
      }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveData = async () => {
      try {
        await dataFormRef.value.validate()
        // 格式化日期为YYYY-MM-DD
        const formattedDate = dataForm.value.date.toISOString().split('T')[0]
        const formData = {
          ...dataForm.value,
          date: formattedDate
        }
        
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/covid-data/${currentId.value}`, formData)
        } else {
          // 添加
          await axios.post('/api/covid-data', formData)
        }
        dialogVisible.value = false
        loadCovidData()
        alert('保存成功')
      } catch (error) {
        console.error('保存疫情数据失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteData = async (id) => {
      if (confirm('确定要删除这条数据吗？')) {
        try {
          await axios.delete(`/api/covid-data/${id}`)
          loadCovidData()
          alert('删除成功')
        } catch (error) {
          console.error('删除疫情数据失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadCovidData()
    })
    
    return {
      covidData,
      dialogVisible,
      dialogTitle,
      dataForm,
      dataFormRef,
      dataRules,
      openAddDialog,
      openEditDialog,
      saveData,
      deleteData
    }
  }
}
</script>

<style scoped>
.covid-data-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>