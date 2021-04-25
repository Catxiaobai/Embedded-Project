<template>
  <div>
    <el-card style="height: 640px">
      <div class="edit_dev">
        <el-transfer
          filterable
          :filter-method="filterMethod"
          filter-placeholder="请输入关键字"
          v-model="value"
          :data="data"
          :titles="['测试用例集', '指令']"
          style="height: 300px"
        >
        </el-transfer>
      </div>
      <el-button type="primary" style="margin-top: 30px; margin-left: 35%" @click="dsp">DSP输入</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Script.vue',
  data() {
    const generateData = (_) => {
      const data = []
      const cities = ['t1,t2,t3,t4', 't5,t6,t7,t8', 't9,t10,t11,t12', 't1,t2,t6,t9', 't8,t7,t3,t4', 't11,t12,t3,t4', 't6,t2,t7,t4']
      const pinyin = ['1', '2', '3', '4', '5', '6', '7']
      cities.forEach((city, index) => {
        data.push({
          label: city,
          key: index,
          pinyin: pinyin[index],
        })
      })
      return data
    }
    return {
      data: generateData(),
      value: [],
      filterMethod(query, item) {
        return item.pinyin.indexOf(query) > -1
      },
    }
  },
  methods: {
    dsp() {
      this.$http
        .get(this.Global_Api + '/api/dsp_test')
        .then((response) => {
          console.log(response.data)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
  },
}
</script>

<style scoped>
.edit_dev >>> .el-transfer-panel {
  width: 350px;
}
</style>
