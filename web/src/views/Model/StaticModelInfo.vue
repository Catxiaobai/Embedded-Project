<template>
  <div>
    <el-card style="height: 634px">
      <el-upload :action="doUpload" :on-success="handleImport" class="inline-block" :show-file-list="false">
        <el-button type="primary">导入</el-button>
      </el-upload>
      <div class="block">
        <el-image :src="src">
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
      src: require('@/assets/images/流程设计图.png'),
    }
  },
  methods: {
    handleImport(res) {
      var base64url = JSON.parse(res.url)
      this.src = 'data:image/png;base64,' + base64url['image_base64_string']
    },
  },
}
</script>

<style scoped></style>
