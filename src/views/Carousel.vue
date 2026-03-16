<template>
  <div class="carousel-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>轮播图管理</span>
          <el-button type="primary" @click="openAddDialog">添加轮播图</el-button>
        </div>
      </template>
      <el-table :data="carousels" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="image_url" label="图片" width="200">
          <template #default="{ row }">
            <el-image :src="row.image_url" :preview-src-list="[row.image_url]" style="width: 100px; height: 60px; object-fit: cover;" />
          </template>
        </el-table-column>
        <el-table-column prop="link" label="链接" />
        <el-table-column prop="order" label="排序" width="80" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-switch v-model="row.status" @change="updateCarousel(row)" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteCarousel(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑轮播图对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="carouselForm" :rules="carouselRules" ref="carouselFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="carouselForm.title" />
        </el-form-item>
        <el-form-item label="图片URL" prop="image_url">
          <el-input v-model="carouselForm.image_url" />
        </el-form-item>
        <el-form-item label="链接" prop="link">
          <el-input v-model="carouselForm.link" />
        </el-form-item>
        <el-form-item label="排序" prop="order">
          <el-input-number v-model="carouselForm.order" :min="0" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="carouselForm.status" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveCarousel">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Carousel',
  setup() {
    const carousels = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加轮播图')
    const carouselForm = ref({
      title: '',
      image_url: '',
      link: '',
      order: 0,
      status: true
    })
    const carouselFormRef = ref(null)
    const currentId = ref(null)
    
    const carouselRules = {
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' }
      ],
      image_url: [
        { required: true, message: '请输入图片URL', trigger: 'blur' }
      ]
    }
    
    const loadCarousels = async () => {
      try {
        const response = await axios.get('/api/carousels/admin')
        carousels.value = response.data
      } catch (error) {
        console.error('加载轮播图失败:', error)
      }
    }
    
    const openAddDialog = () => {
      dialogTitle.value = '添加轮播图'
      carouselForm.value = {
        title: '',
        image_url: '',
        link: '',
        order: 0,
        status: true
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑轮播图'
      carouselForm.value = { ...row }
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveCarousel = async () => {
      try {
        await carouselFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/carousels/${currentId.value}`, carouselForm.value)
        } else {
          // 添加
          await axios.post('/api/carousels', carouselForm.value)
        }
        dialogVisible.value = false
        loadCarousels()
        alert('保存成功')
      } catch (error) {
        console.error('保存轮播图失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const updateCarousel = async (row) => {
      try {
        await axios.put(`/api/carousels/${row.id}`, row)
      } catch (error) {
        console.error('更新轮播图状态失败:', error)
        // 恢复原状态
        row.status = !row.status
      }
    }
    
    const deleteCarousel = async (id) => {
      if (confirm('确定要删除这个轮播图吗？')) {
        try {
          await axios.delete(`/api/carousels/${id}`)
          loadCarousels()
          alert('删除成功')
        } catch (error) {
          console.error('删除轮播图失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadCarousels()
    })
    
    return {
      carousels,
      dialogVisible,
      dialogTitle,
      carouselForm,
      carouselFormRef,
      carouselRules,
      openAddDialog,
      openEditDialog,
      saveCarousel,
      updateCarousel,
      deleteCarousel
    }
  }
}
</script>

<style scoped>
.carousel-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>