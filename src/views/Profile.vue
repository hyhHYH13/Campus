<template>
  <div class="profile-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="个人信息" name="info">
        <el-card>
          <el-form :model="userInfo" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="userInfo.username" disabled />
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="userInfo.name" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email" />
            </el-form-item>
            <el-form-item label="角色">
              <el-input v-model="userInfo.role" disabled />
            </el-form-item>
            <el-form-item label="创建时间">
              <el-input v-model="userInfo.created_at" disabled />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="updateUserInfo">保存修改</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="修改密码" name="password">
        <el-card>
          <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
            <el-form-item label="旧密码" prop="old_password">
              <el-input v-model="passwordForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input v-model="passwordForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="确认新密码" prop="confirm_password">
              <el-input v-model="passwordForm.confirm_password" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Profile',
  setup() {
    const activeTab = ref('info')
    const userInfo = ref({})
    const passwordForm = ref({
      old_password: '',
      new_password: '',
      confirm_password: ''
    })
    const passwordFormRef = ref(null)
    
    const passwordRules = {
      old_password: [
        { required: true, message: '请输入旧密码', trigger: 'blur' }
      ],
      new_password: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '新密码长度至少为6位', trigger: 'blur' }
      ],
      confirm_password: [
        { required: true, message: '请确认新密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== passwordForm.value.new_password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }
    
    const loadUserInfo = async () => {
      try {
        const response = await axios.get('/api/user/me')
        userInfo.value = response.data
        // 格式化创建时间
        if (userInfo.value.created_at) {
          userInfo.value.created_at = new Date(userInfo.value.created_at).toLocaleString()
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
      }
    }
    
    const updateUserInfo = async () => {
      try {
        await axios.put(`/api/users/${userInfo.value.id}`, {
          username: userInfo.value.username,
          name: userInfo.value.name,
          email: userInfo.value.email,
          role: userInfo.value.role
        })
        // 更新本地存储的用户信息
        const userStr = localStorage.getItem('user')
        if (userStr) {
          const user = JSON.parse(userStr)
          user.name = userInfo.value.name
          user.email = userInfo.value.email
          localStorage.setItem('user', JSON.stringify(user))
        }
        alert('个人信息更新成功')
      } catch (error) {
        console.error('更新用户信息失败:', error)
        alert('更新失败，请重试')
      }
    }
    
    const changePassword = async () => {
      try {
        await passwordFormRef.value.validate()
        await axios.post('/api/user/change-password', passwordForm.value)
        alert('密码修改成功')
        // 重置表单
        passwordForm.value = {
          old_password: '',
          new_password: '',
          confirm_password: ''
        }
      } catch (error) {
        console.error('修改密码失败:', error)
        if (error.response && error.response.data) {
          alert(error.response.data.message)
        } else {
          alert('修改密码失败，请重试')
        }
      }
    }
    
    onMounted(() => {
      loadUserInfo()
    })
    
    return {
      activeTab,
      userInfo,
      passwordForm,
      passwordFormRef,
      passwordRules,
      updateUserInfo,
      changePassword
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px 0;
}
</style>