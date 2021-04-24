<template>
  <div id="main" class="el-main-item">
    <el-container style="height: 100%">
      <el-header id="el-header">
        <common-header />
      </el-header>
      <el-container>
        <el-aside id="el-aside">
          <common-aside />
        </el-aside>
        <el-main id="el-main">
          <common-main />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import CommonAside from '@/components/CommonAside'
import CommonHeader from '@/components/CommonHeader'
import CommonMain from '@/components/CommonMain'
export default {
  name: 'ItemMain.vue',
  components: {
    CommonHeader,
    CommonAside,
    CommonMain,
  },
}
</script>

<style scoped>
#el-header {
  padding: 0;
  height: 100px !important;
}
#el-aside {
  width: 300px !important;
}
#el-main {
  padding: 0;
  width: 100%;
  height: 100%;
}
</style>
