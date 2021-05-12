<template>
  <div id="xmi">
    <el-card id="xmi-card" style="height: 653px">
      <el-upload :action="doUpload" :on-success="handleImport" :show-file-list="false">
        <a style="color: #38b2ff; margin-left: 300px"> XMI文件导入</a>
      </el-upload>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'XmiImport',
  data() {
    return {
      doUpload: this.Global_Api + '/api/upload_file',
    }
  },
  methods: {
    handleImport(code, file) {
      this.$http
        .post(this.Global_Api + '/api/import_xmi', { name: file.name, item: this.itemInfo })
        .then((response) => {
          if (response.data.error_code === 0) {
            console.log(response)
            this.$message.success('导入成功')
            this.pageList()
          } else {
            this.$message.error(response.data.error_message)
            this.pageList()
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
  },
}
</script>

<style scoped lang="scss"></style>
