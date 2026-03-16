<template>
  <div class="news-category-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>资讯分类管理</span>
          <el-button type="primary" @click="openAddDialog">添加分类</el-button>
        </div>
      </template>
      <el-table :data="categories" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteCategory(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑分类对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="categoryForm" :rules="categoryRules" ref="categoryFormRef" label-width="100px">
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveCategory">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'NewsCategory',
  setup() {
    const categories = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加分类')
    const categoryForm = ref({
      name: ''
    })
    const categoryFormRef = ref(null)
    const currentId = ref(null)
    
    const categoryRules = {
      name: [
        { required: true, message: '请输入分类名称', trigger: 'blur' }
      ]
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const loadCategories = async () => {
      try {
        const response = await axios.get('/api/news-categories')
        categories.value = response.data
      } catch (error) {
        console.error('加载分类失败:', error)
      }
    }
    
    const openAddDialog = () => {
      dialogTitle.value = '添加分类'
      categoryForm.value = {
        name: ''
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑分类'
      categoryForm.value = { ...row }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveCategory = async () => {
      try {
        await categoryFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/news-categories/${currentId.value}`, categoryForm.value)
        } else {
          // 添加
          await axios.post('/api/news-categories', categoryForm.value)
        }
        dialogVisible.value = false
        loadCategories()
        alert('保存成功')
      } catch (error) {
        console.error('保存分类失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteCategory = async (id) => {
      if (confirm('确定要删除这个分类吗？')) {
        try {
          await axios.delete(`/api/news-categories/${id}`)
          loadCategories()
          alert('删除成功')
        } catch (error) {
          console.error('删除分类失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadCategories()
    })
    
    return {
      categories,
      dialogVisible,
      dialogTitle,
      categoryForm,
      categoryFormRef,
      categoryRules,
      formatDate,
      openAddDialog,
      openEditDialog,
      saveCategory,
      deleteCategory
    }
  }
}
</script>

<style scoped>
.news-category-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>