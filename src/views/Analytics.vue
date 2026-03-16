<template>
  <div class="analytics-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>数据分析</span>
        </div>
      </template>
      
      <!-- 疫情趋势图 -->
      <div class="chart-container">
        <h3>疫情趋势分析</h3>
        <div id="covidTrendChart" ref="covidTrendChart" style="width: 100%; height: 400px;"></div>
      </div>
      
      <!-- 健康状态分布 -->
      <div class="chart-container mt-20">
        <h3>健康状态分布</h3>
        <div id="healthStatusChart" ref="healthStatusChart" style="width: 100%; height: 400px;"></div>
      </div>
      
      <!-- 出入申请统计 -->
      <div class="chart-container mt-20">
        <h3>出入申请统计</h3>
        <div id="entryExitChart" ref="entryExitChart" style="width: 100%; height: 400px;"></div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

export default {
  name: 'Analytics',
  setup() {
    const covidTrendChart = ref(null)
    const healthStatusChart = ref(null)
    const entryExitChart = ref(null)
    let covidChartInstance = null
    let healthChartInstance = null
    let entryExitChartInstance = null
    
    const loadCovidTrendData = async () => {
      try {
        const response = await axios.get('/api/analytics/covid-trend')
        const data = response.data
        
        if (covidChartInstance) {
          covidChartInstance.dispose()
        }
        
        covidChartInstance = echarts.init(covidTrendChart.value)
        
        const option = {
          title: {
            text: '疫情趋势图'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['确诊病例', '康复病例', '死亡病例']
          },
          xAxis: {
            type: 'category',
            data: data.dates
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '确诊病例',
              type: 'line',
              data: data.confirmed,
              itemStyle: {
                color: '#ff4d4f'
              }
            },
            {
              name: '康复病例',
              type: 'line',
              data: data.recovered,
              itemStyle: {
                color: '#52c41a'
              }
            },
            {
              name: '死亡病例',
              type: 'line',
              data: data.deaths,
              itemStyle: {
                color: '#1890ff'
              }
            }
          ]
        }
        
        covidChartInstance.setOption(option)
      } catch (error) {
        console.error('加载疫情趋势数据失败:', error)
      }
    }
    
    const loadHealthStatusData = async () => {
      try {
        const response = await axios.get('/api/analytics/health-status')
        const data = response.data
        
        if (healthChartInstance) {
          healthChartInstance.dispose()
        }
        
        healthChartInstance = echarts.init(healthStatusChart.value)
        
        const option = {
          title: {
            text: '健康状态分布'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: '健康状态',
              type: 'pie',
              radius: '50%',
              data: [
                { value: data.healthy, name: '健康' },
                { value: data.abnormal, name: '异常' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        }
        
        healthChartInstance.setOption(option)
      } catch (error) {
        console.error('加载健康状态数据失败:', error)
      }
    }
    
    const loadEntryExitData = async () => {
      try {
        const response = await axios.get('/api/analytics/entry-exit-stats')
        const data = response.data
        
        if (entryExitChartInstance) {
          entryExitChartInstance.dispose()
        }
        
        entryExitChartInstance = echarts.init(entryExitChart.value)
        
        const option = {
          title: {
            text: '出入申请状态统计'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          xAxis: {
            type: 'category',
            data: ['待审核', '已批准', '已拒绝']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '申请数量',
              type: 'bar',
              data: [data.pending, data.approved, data.rejected],
              itemStyle: {
                color: function(params) {
                  const colors = ['#faad14', '#52c41a', '#ff4d4f']
                  return colors[params.dataIndex]
                }
              }
            }
          ]
        }
        
        entryExitChartInstance.setOption(option)
      } catch (error) {
        console.error('加载出入申请数据失败:', error)
      }
    }
    
    const handleResize = () => {
      covidChartInstance?.resize()
      healthChartInstance?.resize()
      entryExitChartInstance?.resize()
    }
    
    onMounted(() => {
      loadCovidTrendData()
      loadHealthStatusData()
      loadEntryExitData()
      window.addEventListener('resize', handleResize)
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', handleResize)
      covidChartInstance?.dispose()
      healthChartInstance?.dispose()
      entryExitChartInstance?.dispose()
    })
    
    return {
      covidTrendChart,
      healthStatusChart,
      entryExitChart
    }
  }
}
</script>

<style scoped>
.analytics-container {
  padding: 20px 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  margin-top: 20px;
}

.mt-20 {
  margin-top: 20px;
}
</style>