<template>
  <div class="news-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>疫情资讯管理</span>
          <el-button type="primary" @click="openAddDialog">添加资讯</el-button>
        </div>
      </template>
      <el-table :data="newsList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="author" label="作者" width="100" />
        <el-table-column prop="image_url" label="图片" width="150">
          <template #default="{ row }">
            <el-image v-if="row.image_url" :src="row.image_url" :preview-src-list="[row.image_url]" style="width: 80px; height: 60px; object-fit: cover;" />
            <span v-else>无</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteNews(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑资讯对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="800px">
      <el-form :model="newsForm" :rules="newsRules" ref="newsFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="newsForm.title" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="newsForm.category_id">
            <el-option v-for="category in categories" :key="category.id" :label="category.name" :value="category.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="newsForm.content" type="textarea" :rows="10" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="newsForm.author" />
        </el-form-item>
        <el-form-item label="图片URL" prop="image_url">
          <el-input v-model="newsForm.image_url" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveNews">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'News',
  setup() {
    const newsList = ref([])
    const categories = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加资讯')
    const newsForm = ref({
      title: '',
      content: '',
      category_id: '',
      author: '',
      image_url: ''
    })
    const newsFormRef = ref(null)
    const currentId = ref(null)
    
    const newsRules = {
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入内容', trigger: 'blur' }
      ],
      category_id: [
        { required: true, message: '请选择分类', trigger: 'change' }
      ],
      author: [
        { required: true, message: '请输入作者', trigger: 'blur' }
      ]
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const loadNews = async () => {
      try {
        const response = await axios.get('/api/news')
        newsList.value = response.data
      } catch (error) {
        console.error('加载资讯失败:', error)
      }
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
      dialogTitle.value = '添加资讯'
      newsForm.value = {
        title: '',
        content: '',
        category_id: '',
        author: '',
        image_url: ''
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑资讯'
      newsForm.value = { ...row }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveNews = async () => {
      try {
        await newsFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/news/${currentId.value}`, newsForm.value)
        } else {
          // 添加
          await axios.post('/api/news', newsForm.value)
        }
        dialogVisible.value = false
        loadNews()
        alert('保存成功')
      } catch (error) {
        console.error('保存资讯失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteNews = async (id) => {
      if (confirm('确定要删除这篇资讯吗？')) {
        try {
          await axios.delete(`/api/news/${id}`)
          loadNews()
          alert('删除成功')
        } catch (error) {
          console.error('删除资讯失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadNews()
      loadCategories()
    })
    
    return {
      newsList,
      categories,
      dialogVisible,
      dialogTitle,
      newsForm,
      newsFormRef,
      newsRules,
      formatDate,
      openAddDialog,
      openEditDialog,
      saveNews,
      deleteNews
    }
  }
}
</script>

<style scoped>
.news-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>