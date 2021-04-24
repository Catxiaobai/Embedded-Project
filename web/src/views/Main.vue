<template>
  <div id="main">
    <el-container>
      <el-header id="el-header">
        <main-header />
      </el-header>
      <el-main id="el-main">
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import MainHeader from '@/components/MainHeader'

export default {
  name: 'Main.vue',
  components: {
    MainHeader,
  },
}
</script>

<style scoped>
#el-header {
  padding: 0;
  height: 120px !important;
}
#el-main {
  padding: 0;
  width: 100%;
}
</style>
