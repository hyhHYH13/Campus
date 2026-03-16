<template>
  <div class="announcement-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>网站公告管理</span>
          <el-button type="primary" @click="openAddDialog">添加公告</el-button>
        </div>
      </template>
      <el-table :data="announcements" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="content" label="内容" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.content.substring(0, 100) }}...
          </template>
        </el-table-column>
        <el-table-column prop="author" label="发布人" width="120" />
        <el-table-column prop="created_at" label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteAnnouncement(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑公告对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form :model="announcementForm" :rules="announcementRules" ref="announcementFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="announcementForm.title" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="announcementForm.content" type="textarea" :rows="10" />
        </el-form-item>
        <el-form-item label="发布人" prop="author">
          <el-input v-model="announcementForm.author" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveAnnouncement">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Announcement',
  setup() {
    const announcements = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加公告')
    const announcementForm = ref({
      title: '',
      content: '',
      author: ''
    })
    const announcementFormRef = ref(null)
    const currentId = ref(null)
    
    const announcementRules = {
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入内容', trigger: 'blur' }
      ],
      author: [
        { required: true, message: '请输入发布人', trigger: 'blur' }
      ]
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const loadAnnouncements = async () => {
      try {
        const response = await axios.get('/api/announcements')
        announcements.value = response.data
      } catch (error) {
        console.error('加载公告失败:', error)
      }
    }
    
    const openAddDialog = () => {
      dialogTitle.value = '添加公告'
      announcementForm.value = {
        title: '',
        content: '',
        author: ''
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑公告'
      announcementForm.value = { ...row }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveAnnouncement = async () => {
      try {
        await announcementFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/announcements/${currentId.value}`, announcementForm.value)
        } else {
          // 添加
          await axios.post('/api/announcements', announcementForm.value)
        }
        dialogVisible.value = false
        loadAnnouncements()
        alert('保存成功')
      } catch (error) {
        console.error('保存公告失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteAnnouncement = async (id) => {
      if (confirm('确定要删除这个公告吗？')) {
        try {
          await axios.delete(`/api/announcements/${id}`)
          loadAnnouncements()
          alert('删除成功')
        } catch (error) {
          console.error('删除公告失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadAnnouncements()
    })
    
    return {
      announcements,
      dialogVisible,
      dialogTitle,
      announcementForm,
      announcementFormRef,
      announcementRules,
      formatDate,
      openAddDialog,
      openEditDialog,
      saveAnnouncement,
      deleteAnnouncement
    }
  }
}
</script>

<style scoped>
.announcement-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>