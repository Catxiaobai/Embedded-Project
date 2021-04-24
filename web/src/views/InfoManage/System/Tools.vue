<template>
  <div id="tools">
    <el-card style="margin-top: 15%; height: 200px">
      <div id="toolInfo" style="margin-left: 40%; margin-top: 2%">
        <p>当前版本：{{ info.version }}</p>
        <br />
        <p>开发时间：{{ info.time }}</p>
        <br />
        <p>版权所有：{{ info.team }}</p>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Tools.vue',
  data() {
    return {
      info: {
        version: 'V1.0',
        time: '2021年4月',
        team: '中国航空综合技术研究所',
      },
    }
  },
}
</script>

<style scoped></style>
