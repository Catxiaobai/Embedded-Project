<template>
  <div>
    <el-card style="height: 634px">
      <el-upload :action="doUpload" :on-success="handleImport" class="inline-block" :show-file-list="false">
        <el-button type="primary">导入</el-button>
      </el-upload>
      <div class="block" style="margin-top: 30px">
        <el-image :src="src" fit="cover" style="height: 500px">
          <div slot="error" class="image-slot">
            <i class="el-icon-picture-outline"></i>
          </div>
        </el-image>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'StaticModelInfo.vue',
  data() {
    return {
      doUpload: this.Global_Api + '/api/upload_static_model',
      src1: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
      src: '',
      itemInfo: '',
    }
  },
  methods: {
    getItemInfo() {
      this.itemInfo = this.$store.state.item
    },
    init() {
      this.$http.post(this.Global_Api + '/api/load_image', { item: this.itemInfo, name: '静态环境' }).then((response) => {
        console.log(response.data)
        this.src = response.data.src
      })
    },
    handleImport(res) {
      var base64url = JSON.parse(res.url)
      this.src = 'data:image/png;base64,' + base64url['image_base64_string']
      this.$http.post(this.Global_Api + '/api/save_image', { item: this.itemInfo, src: this.src, name: '静态环境' }).then((response) => {
        console.log(response.data)
        this.$message.success('导入成功')
      })
    },
  },
  created() {
    this.getItemInfo()
  },
  mounted() {
    this.init()
  },
}
</script>

<style scoped></style>
