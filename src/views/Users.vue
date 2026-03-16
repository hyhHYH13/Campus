<template>
  <div class="users-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="openAddDialog">添加用户</el-button>
        </div>
      </template>
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)">{{ row.role }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteUser(row.id)" :disabled="row.username === 'admin'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加/编辑用户对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="!!currentId" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!currentId">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveUser">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Users',
  setup() {
    const users = ref([])
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加用户')
    const userForm = ref({
      username: '',
      password: '',
      name: '',
      email: '',
      role: 'user'
    })
    const userFormRef = ref(null)
    const currentId = ref(null)
    
    const userRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6位', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
    
    const getRoleType = (role) => {
      switch (role) {
        case 'admin': return 'danger'
        case 'teacher': return 'warning'
        case 'user': return 'success'
        default: return ''
      }
    }
    
    const loadUsers = async () => {
      try {
        const response = await axios.get('/api/users')
        users.value = response.data
      } catch (error) {
        console.error('加载用户失败:', error)
      }
    }
    
    const openAddDialog = () => {
      dialogTitle.value = '添加用户'
      userForm.value = {
        username: '',
        password: '',
        name: '',
        email: '',
        role: 'user'
      }
      currentId.value = null
      dialogVisible.value = true
    }
    
    const openEditDialog = (row) => {
      dialogTitle.value = '编辑用户'
      userForm.value = { ...row }
      delete userForm.value.password // 编辑时不显示密码
      currentId.value = row.id
      dialogVisible.value = true
    }
    
    const saveUser = async () => {
      try {
        await userFormRef.value.validate()
        if (currentId.value) {
          // 编辑
          await axios.put(`/api/users/${currentId.value}`, userForm.value)
        } else {
          // 添加
          await axios.post('/api/users', userForm.value)
        }
        dialogVisible.value = false
        loadUsers()
        alert('保存成功')
      } catch (error) {
        console.error('保存用户失败:', error)
        alert('保存失败，请重试')
      }
    }
    
    const deleteUser = async (id) => {
      if (confirm('确定要删除这个用户吗？')) {
        try {
          await axios.delete(`/api/users/${id}`)
          loadUsers()
          alert('删除成功')
        } catch (error) {
          console.error('删除用户失败:', error)
          alert('删除失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadUsers()
    })
    
    return {
      users,
      dialogVisible,
      dialogTitle,
      userForm,
      userFormRef,
      userRules,
      currentId,
      formatDate,
      getRoleType,
      openAddDialog,
      openEditDialog,
      saveUser,
      deleteUser
    }
  }
}
</script>

<style scoped>
.users-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>