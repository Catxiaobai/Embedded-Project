<template>
  <div>
    <el-card style="height: 640px">
      <div>
        <a style="font-size: 30px; margin-left: 40%">脚本生成</a>
        <el-card style="margin-top: 30px; height: 300px">
          <div style="white-space: pre-wrap">{{ result }}</div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Script.vue',
  data() {
    return {
      scriptData: '',
      result: '',
      ruleForm: {
        pass: '',
        checkPass: '',
        age: '',
      },
    }
  },
  methods: {
    getScriptData() {
      this.scriptData = this.$store.state.scriptData
      console.log(this.scriptData)
    },
    generate_script() {
      this.$http
        .post(this.Global_Api + '/api/generation/generate_script', this.scriptData)
        .then((response) => {
          console.log(response.data)
          this.result = response.data.result
        })
        .catch(function (error) {
          console.log(error)
        })
    },
  },
  created() {
    this.getScriptData()
  },
  mounted() {
    this.generate_script()
  },
}
</script>

<style scoped>
.edit_dev >>> .el-transfer-panel {
  width: 350px;
}
</style>
